"""
routes.py

Authentication routes for the Expense Tracker application.

Includes:
- User registration
- User login supporting OAuth2 password flow (Swagger UI)
- Password validation for bcrypt (max 72 chars)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from database import SessionLocal
from models import User
from auth.security import hash_password, verify_password
from auth.token import create_access_token

# ---------------------------
# API Router
# ---------------------------
router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------------------
# Database Dependency
# ---------------------------
def get_db():
    """
    Dependency to get a SQLAlchemy database session.

    Yields:
        Session: SQLAlchemy DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Pydantic Schemas
# ---------------------------
class RegisterRequest(BaseModel):
    """
    Schema for user registration request.
    Enforces max password length of 72 for bcrypt.
    """
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=72,
        description="Password (max 72 characters for bcrypt)"
    )

# ---------------------------
# Routes
# ---------------------------
@router.post("/register")
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.

    Steps:
    1. Check if username or email already exists
    2. Hash the password (bcrypt)
    3. Store the user in the database

    Parameters:
        payload (RegisterRequest): Incoming registration data
        db (Session): Database session (dependency)

    Returns:
        dict: Success message

    Raises:
        HTTPException: 400 if user already exists
    """
    # Check if username or email is already registered
    existing = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user instance with hashed password
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )

    # Save user to database
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    Supports OAuth2 password flow for Swagger UI.

    Steps:
    1. Look up user by username
    2. Verify password using bcrypt
    3. Generate JWT token if valid

    Parameters:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password
        db (Session): Database session (dependency)

    Returns:
        dict: JWT token and token type

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Fetch user from database
    user = db.query(User).filter(User.username == form_data.username).first()

    # Verify password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
