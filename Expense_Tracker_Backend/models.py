"""
models.py

Defines SQLAlchemy ORM models for the Expense Tracker application.

Models included:
- User: Stores authentication and user account information
- Expense: Stores expense records linked to a specific user

Relationships:
- One User → Many Expenses
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """
    User model.

    Represents a registered user in the system.
    Used for authentication and authorization.

    Fields:
    - id: Primary key
    - username: Unique username used for login
    - email: Unique email address
    - hashed_password: Securely hashed password
    - expenses: Relationship to Expense model
    """

    __tablename__ = "users"

    # Primary key for the user table
    id = Column(Integer, primary_key=True, index=True)

    # Username used for login (must be unique)
    username = Column(String, unique=True, index=True, nullable=False)

    # Email address of the user (must be unique)
    email = Column(String, unique=True, index=True, nullable=False)

    # Hashed password (NEVER store plain text passwords)
    hashed_password = Column(String, nullable=False)

    # Relationship: one user can have many expenses
    expenses = relationship(
        "Expense",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class Expense(Base):
    """
    Expense model.

    Represents a single expense entry created by a user.

    Fields:
    - id: Primary key
    - title: Short description of the expense
    - amount: Monetary value of the expense
    - category: Category (e.g., Food, Travel)
    - user_id: Foreign key linking to User
    """

    __tablename__ = "expenses"

    # Primary key for the expense table
    id = Column(Integer, primary_key=True, index=True)

    # Short title/description of the expense
    title = Column(String, nullable=False)

    # Expense amount (float for simplicity)
    amount = Column(Float, nullable=False)

    # Category of the expense (optional)
    category = Column(String, nullable=True)

    # Foreign key linking expense to the user who created it
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to User
    owner = relationship("User", back_populates="expenses")
