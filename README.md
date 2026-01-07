# 📊 Expense Tracker (Python CLI)

A production-style Python CLI Expense Tracker that allows users to record, manage, and analyze personal expenses from the command line.

This project demonstrates job-ready software engineering skills, including CLI design, data persistence, logging, and clean Python architecture.

---

## 🚀 Features

- Add new expenses via CLI
- List expenses with optional filters
  - By category
  - By date range
- View expense summaries grouped by category
- Update existing expenses
- Delete expenses
- Persistent storage using JSON
- Application logging

---

## 🛠 Tech Stack

- Language: Python 3
- CLI Parsing: argparse
- Data Storage: JSON
- Logging: Python logging module
- Environment: Python virtual environment (venv)

---

## 📂 Project Structure

Expense_Tracker/
├── venv/ # Virtual environment
├── expense_tracker.py # Main CLI application
├── expenses.json # Persistent expense data
├── logs/
│ └── tracker.log # Application logs
├── README.md # Project documentation

---

## ⚙️ Setup Instructions

### Clone the repository

git clone https://github.com/ykhan-dev/Expense_Tracker.git  
cd Expense_Tracker

### Create and activate virtual environment

python3 -m venv venv  
source venv/bin/activate

### Run the application

python expense_tracker.py --help

---

## 📌 Usage Examples

### Add an expense

python expense_tracker.py add --category Food --description "Lunch at office" --amount 12.50 --date 2025-01-04

### List all expenses

python expense_tracker.py list

### List expenses filtered by category

python expense_tracker.py list --category Food

### List expenses filtered by date range

python expense_tracker.py list --from-date 2025-01-01 --to-date 2025-01-31

### View expense summary

python expense_tracker.py summary

### View summary filtered by category

python expense_tracker.py summary --category Transport

### Update an expense

python expense_tracker.py update --id 3 --amount 60.00 --date 2025-01-06

### Delete an expense

python expense_tracker.py delete --id 5

---

## 📝 Logging

All application activity is logged to:

logs/tracker.log

Includes:

- Expense creation
- Updates
- Deletions
- Errors

---

## 📌 Sample Data (Optional – Best Practice)

For demos or testing, sample data should be populated explicitly using a separate script:

python seed_data.py

This avoids mutating real user data and follows production best practices.

---

## 🎯 Why This Project Matters

This project demonstrates real-world backend engineering concepts:

- Clean CLI architecture
- Argument parsing
- Persistent storage
- Logging
- Maintainable code structure
- Professional documentation

It is designed as a foundation for:

- Database integration
- REST APIs
- Full-stack applications
- AI-enabled analytics

---

## 📈 Future Improvements

- PostgreSQL database integration
- FastAPI backend
- Web frontend
- AI-powered expense insights
- Export to CSV / Excel

---

## 👤 Author

Yousuf Khan  
GitHub: https://github.com/ykhan-dev

---

## ✅ Next Steps

- Push project to GitHub
- Improve commit history
- Add screenshots or demos
- Move to backend API project
