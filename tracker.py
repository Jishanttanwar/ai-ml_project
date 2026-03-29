"""Student Expense Tracker
Author: Jishant Tanwar
Reg. No.: 25BHI10093
"""
import json
import os
import sys
import csv
from datetime import datetime, date
from collections import defaultdict

DATA_FILE = "data/expenses.json"
CATEGORIES = [
    "food",
    "transport",
    "stationery",
    "entertainment",
    "medicine",
    "clothing",
    "recharge",
    "other"
]
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(expenses):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def generate_id(expenses):
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


def add_expense(amount, category, note="", entry_date=None):
    expenses = load_data()

    if category.lower() not in CATEGORIES:
        print(f"  Unknown category '{category}'. Choose from: {', '.join(CATEGORIES)}")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  Amount must be a positive number.")
        return

    if entry_date is None:
        entry_date = str(date.today())
    else:
        try:
            datetime.strptime(entry_date, "%Y-%m-%d")
        except ValueError:
            print("  Date must be in YYYY-MM-DD format.")
            return

    entry = {
        "id": generate_id(expenses),
        "amount": round(amount, 2),
        "category": category.lower(),
        "note": note.strip(),
        "date": entry_date
    }

    expenses.append(entry)
    save_data(expenses)
    print(f"  Added: Rs.{amount:.2f} under '{category}' on {entry_date}")

def list_expenses(filter_category=None, filter_month=None):
    expenses = load_data()

    if not expenses:
        print("  No expenses recorded yet.")
        return

    filtered = expenses

    if filter_category:
        filtered = [e for e in filtered if e["category"] == filter_category.lower()]

    if filter_month:
        filtered = [e for e in filtered if e["date"].startswith(filter_month)]

    if not filtered:
        print("  No matching expenses found.")
        return

    print(f"\n  {'ID':<5} {'Date':<12} {'Category':<14} {'Amount':>10}  {'Note'}")
    print("  " + "-" * 60)
    for e in sorted(filtered, key=lambda x: x["date"]):
        note = e.get("note", "")
        if len(note) > 20:
            note = note[:17] + "..."
        print(f"  {e['id']:<5} {e['date']:<12} {e['category']:<14} Rs.{e['amount']:>7.2f}  {note}")

    total = sum(e["amount"] for e in filtered)
    print("  " + "-" * 60)
    print(f"  {'Total':<5} {'':<12} {'':<14} Rs.{total:>7.2f}")
    print()


def delete_expense(expense_id):
    expenses = load_data()
    try:
        expense_id = int(expense_id)
    except ValueError:
        print("  ID must be an integer.")
        return

    original_len = len(expenses)
    expenses = [e for e in expenses if e["id"] != expense_id]

    if len(expenses) == original_len:
        print(f"  No expense found with ID {expense_id}.")
    else:
        save_data(expenses)
        print(f"  Deleted expense ID {expense_id}.")


def show_summary(filter_month=None):
    expenses = load_data()

    if not expenses:
        print("  No data to summarize.")
        return

    if filter_month:
        expenses = [e for e in expenses if e["date"].startswith(filter_month)]
        if not expenses:
            print(f"  No expenses for {filter_month}.")
            return
        print(f"\n  Summary for {filter_month}:")
    else:
        print("\n  Overall Summary:")

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    total = sum(by_category.values())
    print(f"\n  {'Category':<16} {'Amount':>10}   {'Share':>6}")
    print("  " + "-" * 38)

    for cat, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        pct = (amount / total * 100) if total > 0 else 0
        bar = "#" * int(pct / 5)
        print(f"  {cat:<16} Rs.{amount:>7.2f}   {pct:>5.1f}%  {bar}")

    print("  " + "-" * 38)
    print(f"  {'Total':<16} Rs.{total:>7.2f}")
    print()

def export_csv(output_file="data/expenses_export.csv"):
    expenses = load_data()
    if not expenses:
        print("  Nothing to export.")
        return

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "category", "amount", "note"])
        writer.writeheader()
        writer.writerows(expenses)

    print(f"  Exported {len(expenses)} records to '{output_file}'")

def set_budget(monthly_budget, month=None):
    if month is None:
        month = date.today().strftime("%Y-%m")
    try:
        monthly_budget = float(monthly_budget)
        if monthly_budget <= 0:
            raise ValueError
    except ValueError:
        print("  Budget must be a positive number.")
        return

    budget_file = "data/budgets.json"
    budgets = {}

    if os.path.exists(budget_file):
        with open(budget_file, "r") as f:
            try:
                budgets = json.load(f)
            except json.JSONDecodeError:
                pass

    budgets[month] = monthly_budget

    with open(budget_file, "w") as f:
        json.dump(budgets, f, indent=2)

    print(f"  Budget for {month} set to Rs.{monthly_budget:.2f}")

    expenses = load_data()
    spent = sum(e["amount"] for e in expenses if e["date"].startswith(month))
    remaining = monthly_budget - spent

    if remaining < 0:
        print(f"  WARNING: Already over budget by Rs.{abs(remaining):.2f}!")
    else:
        print(f"  Spent so far: Rs.{spent:.2f} | Remaining: Rs.{remaining:.2f}")


def check_budget(month=None):
    if month is None:
        month = date.today().strftime("%Y-%m")

    budget_file = "data/budgets.json"
    if not os.path.exists(budget_file):
        print("  No budget set. Use: python tracker.py budget <amount>")
        return

    with open(budget_file, "r") as f:
        budgets = json.load(f)

    if month not in budgets:
        print(f"  No budget set for {month}.")
        return

    monthly_budget = budgets[month]
    expenses = load_data()
    spent = sum(e["amount"] for e in expenses if e["date"].startswith(month))
    remaining = monthly_budget - spent
    pct_used = (spent / monthly_budget * 100) if monthly_budget > 0 else 0

    print(f"\n  Budget Status for {month}:")
    print(f"  Budget   : Rs.{monthly_budget:.2f}")
    print(f"  Spent    : Rs.{spent:.2f} ({pct_used:.1f}%)")
    print(f"  Remaining: Rs.{remaining:.2f}")

    bar_filled = int(pct_used / 5)
    bar_empty = 20 - bar_filled
    bar = "[" + "#" * bar_filled + "-" * bar_empty + "]"
    print(f"  {bar} {pct_used:.0f}%")

    if pct_used >= 100:
        print("  Status   : OVER BUDGET")
    elif pct_used >= 80:
        print("  Status   : Approaching limit, be careful!")
    else:
        print("  Status   : On track")
    print()
def print_help():
    print("""
  Student Expense Tracker - Jishant Tanwar (25BHI10093)
  -------------------------------------------------------
  Usage: python tracker.py <command> [options]

  Commands:
    add <amount> <category> [note] [date]   Add a new expense
    list [category] [YYYY-MM]               List expenses (optional filters)
    delete <id>                             Delete an expense by ID
    summary [YYYY-MM]                       Category-wise summary
    budget <amount> [YYYY-MM]               Set monthly budget
    status [YYYY-MM]                        Check budget usage
    export                                  Export to CSV
Categories:
    food, transport, stationery, entertainment,
    medicine, clothing, recharge, other
 Examples:
    python tracker.py add 150 food "lunch at mess"
    python tracker.py add 50 transport "" 2025-03-10
    python tracker.py list
    python tracker.py list food
    python tracker.py list food 2025-03
    python tracker.py summary 2025-03
    python tracker.py budget 3000
    python tracker.py status
    python tracker.py delete 3
    python tracker.py export""")

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("help", "--help", "-h"):
        print_help()
        return

    command = args[0].lower()
    if command == "add":
        if len(args) < 3:
            print("  Usage: python tracker.py add <amount> <category> [note] [date]")
            return
        amount = args[1]
        category = args[2]
        note = args[3] if len(args) > 3 else ""
        entry_date = args[4] if len(args) > 4 else None
        add_expense(amount, category, note, entry_date)

    elif command == "list":
        filter_category = None
        filter_month = None
        for arg in args[1:]:
            if arg.count("-") == 1 and len(arg) == 7:
                filter_month = arg
            else:
                filter_category = arg
        list_expenses(filter_category, filter_month)

    elif command == "delete":
        if len(args) < 2:
            print("  Usage: python tracker.py delete <id>")
            return
        delete_expense(args[1])

    elif command == "summary":
        filter_month = args[1] if len(args) > 1 else None
        show_summary(filter_month)
    elif command == "budget":
        if len(args) < 2:
            print("  Usage: python tracker.py budget <amount> [YYYY-MM]")
            return
        month = args[2] if len(args) > 2 else None
        set_budget(args[1], month)
    elif command == "status":
        filter_month = args[1] if len(args) > 1 else None
        check_budget(filter_month)

    elif command == "export":
        export_csv()
    else:
        print(f"  Unknown command: '{command}'. Run 'python tracker.py help' for usage.")


if __name__ == "__main__":
    main()
