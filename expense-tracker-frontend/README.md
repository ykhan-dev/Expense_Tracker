# Expense Tracker (Full Stack)

A full-stack Expense Tracker application built with **React + Vite** on the frontend and **FastAPI** on the backend. The app supports secure authentication, expense CRUD operations, category-based summaries, and a clean UI.

## Features

**Frontend (React + Vite)**  
- User login with JWT authentication  
- Add, edit, and delete expenses  
- Category-based color coding  
- Expense summary by category and total  
- Loading and empty states  
- Clean, responsive UI  

**Backend (FastAPI)**  
- JWT-based authentication  
- Secure expense CRUD APIs  
- User-scoped expense data  
- SQLite-backed persistence  
- Clean API structure ready for deployment  

## Tech Stack
- Frontend: React, Vite, CSS  
- Backend: FastAPI, Python  
- Authentication: JWT  
- Database: SQLite  

## Project Structure
Expense_Tracker/
├── expense-tracker-frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── Expense_Tracker_Backend/
    ├── app/
    ├── main.py
    ├── requirements.txt
    └── database.db

## Running Locally

**Backend**
```
cd Expense_Tracker_Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs at `http://127.0.0.1:8000`

**Frontend**
```
cd expense-tracker-frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`

## Authentication Flow
- User logs in via the frontend  
- Backend returns a JWT access token  
- Token is stored in `localStorage`  
- All protected expense routes require `Authorization: Bearer <token>`  

## Expense Features
- Add expenses with title, category, and amount  
- Edit existing expenses  
- Delete expenses  
- View category-wise totals  
- View overall total spending  

## Future Enhancements
- Monthly and yearly reports  
- Charts and visual analytics  
- Export expenses to CSV  
- Pagination and filtering  
- Cloud deployment (Docker / AWS / Render)  

## Author
**Yousuf Khan**  
Full-Stack Software Developer
