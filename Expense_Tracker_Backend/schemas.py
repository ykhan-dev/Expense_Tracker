"""
schemas.py

Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

# -------------------------------
# Expense Schemas
# -------------------------------

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str


class ExpenseRead(BaseModel):
    id: int
    title: str
    amount: float
    category: str

    class Config:
        from_attributes = True  # For SQLAlchemy model integration


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None

# -------------------------------
# User Schemas
# -------------------------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
