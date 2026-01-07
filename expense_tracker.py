import json
import os
import logging
import argparse
from datetime import datetime

# --------------------------
# Utility Functions
# --------------------------

def setup_logging():
    """
    Setup logging for the Expense Tracker.
    Creates the logs folder if it doesn't exist and configures logging format.
    """
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/tracker.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def reset_expenses(_args):
    """
    Delete all expenses from the expenses.json file.
    """
    confirm = input(
        "⚠️  This will permanently delete ALL expenses. Type 'YES' to confirm: "
    )

    if confirm != "YES":
        print("Reset cancelled.")
        return

    save_expenses([])
    logging.warning("All expenses were deleted by user.")
    print("✅ All expenses have been deleted.")


def load_expenses(file_path="expenses.json"):
    """
    Load expenses from the JSON file.
    Returns an empty list if the file doesn't exist.
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

def save_expenses(expenses, file_path="expenses.json"):
    """
    Save expenses to the JSON file.
    """
    with open(file_path, "w") as f:
        json.dump(expenses, f, indent=4)

# --------------------------
# Core Functions
# --------------------------

def add_expense(args):
    """
    Add a new expense entry to expenses.json.
    """
    expenses = load_expenses()
    expense_id = max([e["id"] for e in expenses], default=0) + 1
    expense = {
        "id": expense_id,
        "date": args.date or datetime.now().strftime("%Y-%m-%d"),
        "category": args.category,
        "description": args.description,
        "amount": args.amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    logging.info(f"Added expense: {expense}")
    print(f"Expense added: {expense}")

def list_expenses(args):
    """
    List all expenses, optionally filtered by category or date range.
    """
    expenses = load_expenses()
    filtered = []
    for e in expenses:
        if args.category and e["category"].lower() != args.category.lower():
            continue
        if args.from_date and e["date"] < args.from_date:
            continue
        if args.to_date and e["date"] > args.to_date:
            continue
        filtered.append(e)

    if not filtered:
        print("No expenses found for the given filters.")
        return

    for e in filtered:
        print(f"{e['id']}. {e['date']} | {e['category']} | {e['description']} | ${e['amount']}")

def summary_expenses(args):
    """
    Print a summary of total expenses grouped by category.
    Can be filtered by category or date range.
    """
    expenses = load_expenses()
    summary = {}

    for e in expenses:
        if args.category and e["category"].lower() != args.category.lower():
            continue
        if args.from_date and e["date"] < args.from_date:
            continue
        if args.to_date and e["date"] > args.to_date:
            continue
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    if not summary:
        print("No expenses to summarize for the given filters.")
        return

    print("Expense Summary:")
    for category, total in summary.items():
        print(f"{category}: ${total:.2f}")

def update_expense(args):
    """
    Update an existing expense by ID.
    """
    expenses = load_expenses()
    for e in expenses:
        if e["id"] == args.id:
            if args.category:
                e["category"] = args.category
            if args.description:
                e["description"] = args.description
            if args.amount is not None:
                e["amount"] = args.amount
            if args.date:
                e["date"] = args.date
            save_expenses(expenses)
            logging.info(f"Updated expense: {e}")
            print(f"Expense updated: {e}")
            return
    print(f"No expense found with ID {args.id}")

def delete_expense(args):
    """
    Delete an expense by ID.
    """
    expenses = load_expenses()
    for e in expenses:
        if e["id"] == args.id:
            expenses.remove(e)
            save_expenses(expenses)
            logging.info(f"Deleted expense: {e}")
            print(f"Deleted expense: {e}")
            return
    print(f"No expense found with ID {args.id}")

# --------------------------
# Main CLI
# --------------------------

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Reset command
    reset_parser = subparsers.add_parser("reset",help="Delete all expenses")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--category", required=True, help="Expense category")
    add_parser.add_argument("--description", required=True, help="Expense description")
    add_parser.add_argument("--amount", type=float, required=True, help="Expense amount")
    add_parser.add_argument("--date", help="Expense date (YYYY-MM-DD)")

    # List command
    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--from-date", help="Start date (YYYY-MM-DD)")
    list_parser.add_argument("--to-date", help="End date (YYYY-MM-DD)")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Summary of expenses")
    summary_parser.add_argument("--category", help="Filter by category")
    summary_parser.add_argument("--from-date", help="Start date (YYYY-MM-DD)")
    summary_parser.add_argument("--to-date", help="End date (YYYY-MM-DD)")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an expense by ID")
    update_parser.add_argument("--id", type=int, required=True, help="Expense ID to update")
    update_parser.add_argument("--category", help="New category")
    update_parser.add_argument("--description", help="New description")
    update_parser.add_argument("--amount", type=float, help="New amount")
    update_parser.add_argument("--date", help="New date (YYYY-MM-DD)")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("--id", type=int, required=True, help="Expense ID to delete")

    args = parser.parse_args()

    # Execute command
    if args.command == "add":
        add_expense(args)
    elif args.command == "list":
        list_expenses(args)
    elif args.command == "summary":
        summary_expenses(args)
    elif args.command == "update":
        update_expense(args)
    elif args.command == "delete":
        delete_expense(args)
    elif args.command == "reset":
        reset_expenses(args)


# --------------------------
# Sample Expenses for Testing
# --------------------------
if __name__ == "__main__":
    main()
