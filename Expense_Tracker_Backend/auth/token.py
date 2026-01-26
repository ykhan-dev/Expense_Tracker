"""
token.py

Handles JWT token creation, verification, and current user retrieval for authentication.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

# -------------------------------
# JWT Configuration
# -------------------------------
SECRET_KEY = "your_super_secret_key"  # Replace with a strong secret in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token validity duration

# OAuth2 scheme for FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------------
# Database session dependency
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# Token creation
# -------------------------------
def create_access_token(data: dict, expires_delta: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Create a JWT access token.

    Parameters:
        data (dict): Data to encode in the token (e.g., {"sub": username}).
        expires_delta (int, optional): Expiration time in minutes.

    Returns:
        str: JWT token string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# -------------------------------
# Token verification
# -------------------------------
def verify_access_token(token: str) -> dict:
    """
    Verify a JWT access token.

    Parameters:
        token (str): JWT token string.

    Returns:
        dict: Decoded payload.

    Raises:
        JWTError: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("Invalid or expired token")


# -------------------------------
# Current user dependency
# -------------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decode JWT token and return the current user.

    Parameters:
        token (str): JWT token provided in Authorization header.
        db (Session): Database session.

    Returns:
        User: SQLAlchemy User object.

    Raises:
        HTTPException: 401 if token is invalid or user does not exist.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


