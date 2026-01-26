# Expense Tracker Backend

A FastAPI-based backend for an Expense Tracker application.
This project demonstrates clean backend architecture, JWT authentication,
secure password handling, and database operations using SQLAlchemy.

---

## Features

- User registration and login
- JWT-based authentication
- Secure password hashing with bcrypt
- Expense CRUD operations
- SQLAlchemy ORM
- Modular and scalable project structure

---

## Project Structure

Expense_Tracker_Backend/
├── auth/
│ ├── **init**.py
│ ├── routes.py
│ ├── security.py
│ └── token.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
└── README.md

---

## Setup Instructions

### 1. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate

---

### 2. Install dependencies

pip install -r requirements.txt

---

### 3. Run the development server

uvicorn main:app --reload

The server will start at:

http://127.0.0.1:8000

---

## API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI:
  http://127.0.0.1:8000/docs

- OpenAPI JSON:
  http://127.0.0.1:8000/openapi.json

---

## Dependencies

| Package         | Purpose               |
| --------------- | --------------------- |
| fastapi         | API framework         |
| uvicorn         | ASGI server           |
| sqlalchemy      | Database ORM          |
| psycopg2-binary | PostgreSQL driver     |
| passlib         | Password hashing      |
| python-jose     | JWT authentication    |
| pydantic        | Data validation       |
| email-validator | Email validation      |
| python-dotenv   | Environment variables |

---

## Notes

- SQLite can be used for local development and testing
- PostgreSQL is recommended for production use
- Never commit secrets (JWT keys, database URLs) to source control
- Use environment variables or a .env file for configuration

---

## Author

Yousuf

---

## Next Improvements

- Add Alembic for database migrations
- Add automated tests using pytest
- Add Docker and Docker Compose support
- Implement role-based access control
