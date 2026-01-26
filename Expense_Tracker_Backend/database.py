# database.py
"""
database.py

Handles PostgreSQL database connection using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection URL
# Replace "postgres" with your PostgreSQL username and password if different
DATABASE_URL = "postgresql://fykhan@localhost/expense_tracker_db"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal class for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
