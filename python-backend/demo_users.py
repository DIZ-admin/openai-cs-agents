"""
Demo Users Database for Development and Testing

⚠️ WARNING: This file is for DEVELOPMENT and TESTING purposes ONLY!
⚠️ DO NOT use these credentials in production environments!

This module contains hardcoded demo user accounts with known passwords
for local development and automated testing. These users are automatically
loaded when ENVIRONMENT=development.

Demo Credentials:
-----------------
Username: admin
Password: secret
Roles: admin, user

Username: demo
Password: secret
Roles: user

Security Notes:
---------------
1. These users are ONLY loaded when ENVIRONMENT=development
2. Password hashes are bcrypt hashes of "secret"
3. In production, use a real database with proper user management
4. Never commit real user credentials to version control
5. Always use strong, unique passwords in production

Usage:
------
This module is automatically imported by auth.py when running in
development mode. No manual import is needed.
"""

from typing import Optional

# Demo users database with bcrypt-hashed passwords
# Password for all demo users: "secret"
# Hash generated with: bcrypt.hashpw(b"secret", bcrypt.gensalt())
DEMO_USERS_DB = {
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


def get_demo_users():
    """
    Get demo users database.
    
    Returns:
        dict: Demo users database with username as key
        
    Security:
        This function should only be called in development environments.
        The calling code is responsible for checking ENVIRONMENT variable.
    """
    return DEMO_USERS_DB


def is_demo_user(username: str) -> bool:
    """
    Check if a username is a demo user.
    
    Args:
        username: Username to check
        
    Returns:
        bool: True if username is a demo user, False otherwise
    """
    return username in DEMO_USERS_DB


def get_demo_user(username: str) -> Optional[dict]:
    """
    Get a demo user by username.

    Args:
        username: Username to retrieve

    Returns:
        Optional[dict]: User data if found, None otherwise
    """
    return DEMO_USERS_DB.get(username)

