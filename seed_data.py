import os
import json

# Path to your expenses JSON
EXPENSES_FILE = "expenses.json"

# Sample expenses
sample_expenses = [
    {"id": 1, "date": "2025-01-04", "category": "Food", "description": "Lunch at office", "amount": 12.5},
    {"id": 2, "date": "2025-01-05", "category": "Transport", "description": "Uber to client meeting", "amount": 20.0},
    {"id": 3, "date": "2025-01-06", "category": "Utilities", "description": "Internet bill - monthly", "amount": 55.0},
    {"id": 4, "date": "2025-01-07", "category": "Software", "description": "VS Code extension subscription", "amount": 9.99},
    {"id": 5, "date": "2025-01-08", "category": "Food", "description": "Cafe lunch", "amount": 12.5},
    {"id": 6, "date": "2025-01-09", "category": "Transport", "description": "Taxi to office", "amount": 8.0},
    {"id": 7, "date": "2025-01-10", "category": "Utilities", "description": "Electricity bill", "amount": 45.0},
    {"id": 8, "date": "2025-01-11", "category": "Food", "description": "Dinner at restaurant", "amount": 20.0},
    {"id": 9, "date": "2025-01-12", "category": "Subscription", "description": "Netflix", "amount": 15.0},
    {"id": 10, "date": "2025-01-13", "category": "Transport", "description": "Bus pass", "amount": 30.0},
]

# Save to JSON
with open(EXPENSES_FILE, "w") as f:
    json.dump(sample_expenses, f, indent=4)

print(f"✅ {len(sample_expenses)} sample expenses written to {EXPENSES_FILE}")
