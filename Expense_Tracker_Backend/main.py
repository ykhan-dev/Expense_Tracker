"""
main.py

FastAPI application for Expense Tracker with PostgreSQL and JWT Authentication.

Features:
- Expense CRUD endpoints (Create, Read, Update, Delete)
- User registration and login via auth router
- JWT token authentication for protected routes
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, SessionLocal
from models import Expense
from schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from auth.routes import router as auth_router
from auth.token import get_current_user

# --------------------------------------------------
# Database Setup
# --------------------------------------------------
# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# --------------------------------------------------
# FastAPI App Initialization
# --------------------------------------------------
app = FastAPI(title="Expense Tracker API", version="1.0.0")

# --------------------------------------------------
# CORS Middleware (REQUIRED for frontend)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes from auth.router
app.include_router(auth_router)


# --------------------------------------------------
# Database Dependency
# --------------------------------------------------
def get_db():
    """
    Provide a SQLAlchemy database session to routes.

    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Expense Endpoints (JWT Protected)
# --------------------------------------------------

@app.post("/expenses", response_model=ExpenseRead)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Create a new expense for the authenticated user.

    Steps:
    1. Receive expense data from request body.
    2. Associate the expense with the current user's ID.
    3. Add and commit the new expense to the database.
    4. Return the created expense.
    """
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        user_id=current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)  # Refresh to get auto-generated fields like ID
    return new_expense


@app.get("/expenses", response_model=List[ExpenseRead])
def get_expenses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retrieve all expenses for the authenticated user.

    Steps:
    1. Query the database for expenses matching the current user's ID.
    2. Return the list of expenses.
    """
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses


@app.get("/expenses/{expense_id}", response_model=ExpenseRead)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retrieve a single expense by ID for the authenticated user.

    Steps:
    1. Query the database for the expense by ID and user ID.
    2. If the expense does not exist, raise HTTP 404.
    3. Return the expense.
    """
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseRead)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Update an existing expense for the authenticated user.

    Steps:
    1. Retrieve the expense by ID and user ID.
    2. If not found, raise HTTP 404.
    3. Update only the fields provided in the request body.
    4. Commit changes to the database.
    5. Return the updated expense.
    """
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Update only the fields that are provided in the request
    for field, value in expense_data.dict(exclude_unset=True).items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Delete an expense by ID for the authenticated user.

    Steps:
    1. Retrieve the expense by ID and user ID.
    2. If not found, raise HTTP 404.
    3. Delete the expense from the database.
    4. Commit the transaction.
    5. Return a success message.
    """
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}
