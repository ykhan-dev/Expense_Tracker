"""
auth/security.py

Security utilities for authentication and authorization.

This module is responsible for:
- Securely hashing user passwords
- Verifying passwords during login
- Centralizing all password-related logic

Why Argon2?
-----------
Argon2 is a modern, memory-hard password hashing algorithm and is
recommended by OWASP. It avoids bcrypt limitations such as:
- 72-byte password length limit
- Compatibility issues with newer Python versions (e.g. Python 3.14)
"""

from passlib.context import CryptContext


# -------------------------------------------------------------------
# Password hashing configuration
# -------------------------------------------------------------------
# We use Argon2 for password hashing:
# - Secure against GPU attacks
# - No password length limit
# - Fully supported by passlib
# -------------------------------------------------------------------
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


# -------------------------------------------------------------------
# Password hashing
# -------------------------------------------------------------------
def hash_password(password: str) -> str:
    """
    Hash a plaintext password using Argon2.

    This function should be called:
    - When a user registers
    - When a password is changed or reset

    Args:
        password (str): Plaintext password provided by the user

    Returns:
        str: Secure Argon2 hash of the password
    """
    return pwd_context.hash(password)


# -------------------------------------------------------------------
# Password verification
# -------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored password hash.

    This function should be called:
    - During user login
    - When re-authentication is required

    Args:
        plain_password (str): Password provided by the user
        hashed_password (str): Stored hashed password from the database

    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
