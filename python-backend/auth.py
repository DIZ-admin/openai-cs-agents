"""
JWT Authentication Module for ERNI Gruppe Building Agents API.

This module provides JWT-based authentication for securing API endpoints.
It includes token generation, validation, and user management.

Security Features:
- JWT tokens with configurable expiration
- Password hashing with bcrypt
- Token refresh mechanism
- Role-based access control (RBAC) support
- Secure secret key management

Usage:
    from auth import get_current_user, create_access_token
    
    # In API endpoint:
    @app.post("/protected")
    async def protected_route(current_user: str = Depends(get_current_user)):
        return {"user": current_user}
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ============================================================================
# Configuration
# ============================================================================

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production-NEVER-USE-IN-PROD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer security scheme
security = HTTPBearer()

# ============================================================================
# Pydantic Models
# ============================================================================

class Token(BaseModel):
    """JWT token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """JWT token payload data."""
    username: Optional[str] = None
    roles: Optional[list[str]] = None


class User(BaseModel):
    """User model for authentication."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    roles: list[str] = ["user"]


class UserInDB(User):
    """User model with hashed password (for database storage)."""
    hashed_password: str


# ============================================================================
# Mock User Database (Replace with real database in production)
# ============================================================================

# WARNING: This is a mock database for demonstration purposes only.
# In production, replace this with a real database (PostgreSQL, MongoDB, etc.)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@erni-gruppe.ch",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
        "roles": ["admin", "user"],
    },
    "demo": {
        "username": "demo",
        "full_name": "Demo User",
        "email": "demo@erni-gruppe.ch",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
        "roles": ["user"],
    },
}


# ============================================================================
# Password Utilities
# ============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password
        hashed_password: Bcrypt hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Bcrypt hashed password
    """
    return pwd_context.hash(password)


# ============================================================================
# User Management
# ============================================================================

def get_user(username: str) -> Optional[UserInDB]:
    """
    Retrieve user from database by username.
    
    Args:
        username: Username to lookup
        
    Returns:
        UserInDB object if found, None otherwise
    """
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate user with username and password.
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        UserInDB object if authentication successful, None otherwise
    """
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ============================================================================
# JWT Token Management
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData object if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: list = payload.get("roles", ["user"])
        
        if username is None:
            return None
            
        return TokenData(username=username, roles=roles)
    except JWTError:
        return None


# ============================================================================
# FastAPI Dependencies
# ============================================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    FastAPI dependency to get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data is None or token_data.username is None:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    FastAPI dependency to get current active (non-disabled) user.
    
    Args:
        current_user: Current user from get_current_user dependency
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user is disabled
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ============================================================================
# Role-Based Access Control (RBAC)
# ============================================================================

def require_role(required_role: str):
    """
    FastAPI dependency factory for role-based access control.
    
    Usage:
        @app.get("/admin")
        async def admin_route(user: User = Depends(require_role("admin"))):
            return {"message": "Admin access granted"}
    
    Args:
        required_role: Role required to access the endpoint
        
    Returns:
        FastAPI dependency function
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if required_role not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role: {required_role}"
            )
        return current_user
    
    return role_checker

