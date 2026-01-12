import json
import csv
import os
import logging
import argparse
from datetime import datetime

# --------------------------
# Utility Functions
# --------------------------
def validate_date(date_str):
    """
    Validate date format YYYY-MM-DD.
    Returns True if valid, otherwise False.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_amount(amount):
    """
    Ensure amount is a positive number.
    """
    return amount > 0


def export_expenses(args):
    """
    Export expenses to a CSV file.

    Features:
    - Optional filters: category, from-date, to-date
    - Optional custom output filename (--output)
    - Prevents accidental overwrites
    """

    # Load all expenses from JSON
    expenses = load_expenses()

    if not expenses:
        print("❌ No expenses to export.")
        return

    # ✅ VALIDATE FILTERS
    if args.from_date:
        from_date = validate_date(args.from_date)

    if args.to_date:
        to_date = validate_date(args.to_date)

    if args.category:
        category = args.category.lower()


    # Guard clause: no data to export
    if not expenses:
        print("❌ No expenses to export.")
        return

    # Filter by category if provided
    if args.category:
        expenses = [
            e for e in expenses
            if e["category"].lower() == args.category.lower()
        ]

    # Filter by start date if provided
    if args.from_date:
        try:
            from_date = datetime.strptime(args.from_date, "%Y-%m-%d").date()
            expenses = [
                e for e in expenses
                if datetime.strptime(e["date"], "%Y-%m-%d").date() >= from_date
            ]
        except ValueError:
            print("❌ Invalid from-date format. Use YYYY-MM-DD.")
            return

    # Filter by end date if provided
    if args.to_date:
        try:
            to_date = datetime.strptime(args.to_date, "%Y-%m-%d").date()
            expenses = [
                e for e in expenses
                if datetime.strptime(e["date"], "%Y-%m-%d").date() <= to_date
            ]
        except ValueError:
            print("❌ Invalid to-date format. Use YYYY-MM-DD.")
            return

    # Use custom filename if provided, otherwise default to "expenses.csv"
    filename = args.output if args.output else "expenses.csv"

    # Prevent overwriting an existing export file
    if os.path.exists(filename):
        print(
            f"❌ {filename} already exists. "
            "Delete it first if you want to re-export."
        )
        return

    # Currently we only support CSV
    if args.format == "csv":
        try:
            # Open file for writing (newline='' avoids blank rows on Windows)
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                # Create a CSV writer using dictionary keys
                writer = csv.DictWriter(
                    file,
                    fieldnames=["id", "date", "category", "description", "amount"]
                )
                # Write header row
                writer.writeheader()
                # Write all filtered expense rows
                writer.writerows(expenses)

            # User feedback
            print(f"✅ Expenses exported successfully to {filename}")
        except Exception as e:
            print(f"❌ Failed to export expenses: {e}")


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


def clear_all_expenses():
    """
    Delete all expenses by saving an empty list to expenses.json.
    """
    save_expenses([])


def reset_expenses(_args):
    """
    Reset (delete) all expenses from the expenses.json file after user confirmation.
    """
    
    # Load existing expenses
    expenses = load_expenses()

    # If there are no expenses, do nothing
    if not expenses:
        print("ℹ️  No expenses found. Nothing to reset.")
        return

    # Ask for confirmation
    confirm = input(
        "⚠️  This will permanently delete ALL expenses. Are your sure? (yes/no)  "
    )

    # Normalize input (case-insensitive, trims spaces)
    if confirm.strip().lower() in ( "yes", "y"):
        clear_all_expenses()
        logging.warning("All expenses were deleted by user.")
        print("✅ All expenses have been deleted.")
    else:
        print("❌ Reset cancelled.")
        return
   

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
    
    # ✅ VALIDATION (early)
    try:
        date = validate_date(args.date)
        amount = validate_amount(args.amount)
    except ValueError as e:
        print(f"❌ {e}")
        return

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
    if not expenses:
        print("No expenses found.")
        return

    # ✅ FILTER VALIDATION (only if provided)
    if args.from_date:
        from_date = validate_date(args.from_date)

    if args.to_date:
        to_date = validate_date(args.to_date)

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

    if args.category:
        category = args.category.lower()

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

    # Create a new subcommand: `export`
    # This allows users to run:
    #   python expense_tracker.py export ...
    export_parser = subparsers.add_parser(
        "export",
        help="Export expenses to a file"
    )

    # Required argument that defines the export format
    # For now, we only support CSV, but this is future-proof
    # (JSON, Excel, etc. can be added later)
    export_parser.add_argument(
        "--format",
        choices=["csv"],
        required=True,
        help="Export format (currently only csv supported)"
    )

    # Optional output filename
    # Example:
    #   python expense_tracker.py export --format csv --output jan_expenses.csv
    export_parser.add_argument(
        "--output",
        help="Output file name (default: expenses.csv)"
    )

    # Optional filter: export only expenses from a specific category
    # Example:
    #   python expense_tracker.py export --format csv --category Food
    export_parser.add_argument(
        "--category",
        help="Filter expenses by category"
    )

    # Optional filter: start date for export range
    # Only expenses on or after this date will be exported
    # Date format: YYYY-MM-DD
    export_parser.add_argument(
        "--from-date",
        help="Start date (YYYY-MM-DD)"
    )

    # Optional filter: end date for export range
    # Only expenses on or before this date will be exported
    # Date format: YYYY-MM-DD
    export_parser.add_argument(
        "--to-date",
        help="End date (YYYY-MM-DD)"
    )


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
    elif args.command == "export":
        export_expenses(args)



# --------------------------
# Sample Expenses for Testing
# --------------------------
if __name__ == "__main__":
    main()
