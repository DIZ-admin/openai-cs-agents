"""
Unit tests for authentication module.

Tests JWT token generation, validation, password hashing, and user authentication.
"""

import pytest
from datetime import timedelta
from fastapi import HTTPException

from auth import (
    verify_password,
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    decode_access_token,
    get_current_user,
    TokenData,
    User,
    UserInDB,
)


# ============================================================================
# Password Hashing Tests
# ============================================================================

class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_password_hash_and_verify(self):
        """Test that password hashing and verification work correctly."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Verification should succeed
        assert verify_password(password, hashed) is True

    def test_password_verify_wrong_password(self):
        """Test that verification fails with wrong password."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_password_hash_different_each_time(self):
        """Test that same password produces different hashes (salt)."""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


# ============================================================================
# User Management Tests
# ============================================================================

class TestUserManagement:
    """Test user retrieval and authentication."""

    def test_get_user_existing(self):
        """Test retrieving an existing user."""
        user = get_user("demo")
        
        assert user is not None
        assert isinstance(user, UserInDB)
        assert user.username == "demo"
        assert user.email == "demo@erni-gruppe.ch"
        assert user.disabled is False
        assert "user" in user.roles

    def test_get_user_nonexistent(self):
        """Test retrieving a non-existent user."""
        user = get_user("nonexistent_user")
        assert user is None

    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        user = authenticate_user("demo", "secret")
        
        assert user is not None
        assert isinstance(user, UserInDB)
        assert user.username == "demo"

    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password."""
        user = authenticate_user("demo", "wrong_password")
        assert user is None

    def test_authenticate_user_nonexistent(self):
        """Test authentication with non-existent user."""
        user = authenticate_user("nonexistent", "password")
        assert user is None

    def test_admin_user_has_admin_role(self):
        """Test that admin user has admin role."""
        user = get_user("admin")
        
        assert user is not None
        assert "admin" in user.roles
        assert "user" in user.roles


# ============================================================================
# JWT Token Tests
# ============================================================================

class TestJWTTokens:
    """Test JWT token creation and validation."""

    def test_create_access_token(self):
        """Test creating a JWT access token."""
        data = {"sub": "testuser", "roles": ["user"]}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiration(self):
        """Test creating token with custom expiration."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        assert token is not None
        assert isinstance(token, str)

    def test_decode_access_token_valid(self):
        """Test decoding a valid JWT token."""
        data = {"sub": "testuser", "roles": ["user", "admin"]}
        token = create_access_token(data)
        
        token_data = decode_access_token(token)
        
        assert token_data is not None
        assert isinstance(token_data, TokenData)
        assert token_data.username == "testuser"
        assert token_data.roles == ["user", "admin"]

    def test_decode_access_token_invalid(self):
        """Test decoding an invalid JWT token."""
        invalid_token = "invalid.token.here"
        token_data = decode_access_token(invalid_token)
        
        assert token_data is None

    def test_decode_access_token_missing_sub(self):
        """Test decoding token without 'sub' claim."""
        data = {"other_field": "value"}
        token = create_access_token(data)
        
        token_data = decode_access_token(token)
        assert token_data is None

    def test_token_contains_expiration(self):
        """Test that token contains expiration claim."""
        from jose import jwt
        from auth import SECRET_KEY, ALGORITHM

        data = {"sub": "testuser"}
        token = create_access_token(data)

        # Decode without verification to inspect payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert "exp" in payload
        assert "iat" in payload
        assert payload["sub"] == "testuser"


# ============================================================================
# FastAPI Dependency Tests
# ============================================================================

class TestFastAPIDependencies:
    """Test FastAPI dependency functions."""

    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self):
        """Test getting current user with valid token."""
        from fastapi.security import HTTPAuthorizationCredentials
        
        # Create token for existing user
        token = create_access_token({"sub": "demo", "roles": ["user"]})
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        user = await get_current_user(credentials)
        
        assert user is not None
        assert isinstance(user, User)
        assert user.username == "demo"
        assert user.disabled is False

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token."""
        from fastapi.security import HTTPAuthorizationCredentials
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid.token.here"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_current_user_nonexistent_user(self):
        """Test getting current user for non-existent user."""
        from fastapi.security import HTTPAuthorizationCredentials
        
        # Create token for non-existent user
        token = create_access_token({"sub": "nonexistent", "roles": ["user"]})
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_get_current_user_disabled_user(self):
        """Test getting current user for disabled user."""
        from fastapi.security import HTTPAuthorizationCredentials
        from auth import fake_users_db
        
        # Temporarily create a disabled user
        fake_users_db["disabled_user"] = {
            "username": "disabled_user",
            "full_name": "Disabled User",
            "email": "disabled@test.com",
            "hashed_password": get_password_hash("password"),
            "disabled": True,
            "roles": ["user"],
        }
        
        try:
            token = create_access_token({"sub": "disabled_user", "roles": ["user"]})
            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=token
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(credentials)
            
            assert exc_info.value.status_code == 403
            assert "disabled" in exc_info.value.detail.lower()
        finally:
            # Clean up
            del fake_users_db["disabled_user"]


# ============================================================================
# Integration Tests
# ============================================================================

class TestAuthenticationFlow:
    """Test complete authentication flow."""

    @pytest.mark.asyncio
    async def test_complete_auth_flow(self):
        """Test complete authentication flow from login to API access."""
        from fastapi.security import HTTPAuthorizationCredentials
        
        # Step 1: Authenticate user
        user = authenticate_user("demo", "secret")
        assert user is not None
        
        # Step 2: Create access token
        token = create_access_token(
            data={"sub": user.username, "roles": user.roles}
        )
        assert token is not None
        
        # Step 3: Decode token
        token_data = decode_access_token(token)
        assert token_data is not None
        assert token_data.username == "demo"
        
        # Step 4: Get current user from token
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        current_user = await get_current_user(credentials)
        assert current_user.username == "demo"
        assert current_user.email == "demo@erni-gruppe.ch"

    def test_password_change_invalidates_old_tokens(self):
        """Test that changing password should invalidate old tokens."""
        # This is a conceptual test - in production, implement token revocation
        # For now, we just verify that new password creates different hash
        
        old_password = "old_password"
        new_password = "new_password"
        
        old_hash = get_password_hash(old_password)
        new_hash = get_password_hash(new_password)
        
        # Hashes should be different
        assert old_hash != new_hash
        
        # Old password should not verify against new hash
        assert verify_password(old_password, new_hash) is False
        
        # New password should verify against new hash
        assert verify_password(new_password, new_hash) is True

