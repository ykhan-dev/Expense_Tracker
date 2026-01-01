# expense_tracker.py

def add_expense():
    print("Adding a new expense...")

def view_expenses():
    print("Listing all expenses...")

def delete_expense():
    print("Deleting an expense...")

def show_summary():
    print("Showing summary of expenses...")

def main():
    print("Welcome to your CLI Expense Tracker!")
    while True:
        print("\nPlease choose an option:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Show Summary")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
