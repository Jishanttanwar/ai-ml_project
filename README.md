# ai-ml_project
# Student Expense Tracker

A command-line tool built in Python to help college students track daily expenses, set monthly budgets, and understand their spending patterns.

**Author:** Jishant Tanwar  
**Reg. No.:** 25BHI10093  




## Why I Built This

Living in a hostel on a fixed monthly allowance, I kept running out of money before the month ended and had no idea where it was all going. I built this tool to log expenses quickly, categorize them, and check how much budget is left — all from the terminal, no app or internet needed.



## Features

- Add, list, and delete expense entries
- Organize spending into categories (food, transport, stationery, etc.)
- Monthly budget tracking with usage bar
- Category-wise summary with percentage breakdown
- Filter expenses by category or month
- Export data to CSV for use in Excel/Sheets
- All data stored locally as JSON — no cloud, no account

---

## Requirements

- Python 3.7 or above
- No external libraries required (uses only Python standard library)

---

## Setup

1. Clone or download the repository:

```bash
git clone https://github.com/jishanttanwar/student-expense-tracker.git
cd student-expense-tracker
```

2. That's it. No installation needed.

To verify everything works:

```bash
python test_tracker.py
```

---

## Usage

### Add an Expense

```bash
python tracker.py add <amount> <category> [note] [date]
```

Examples:
```bash
python tracker.py add 150 food "lunch at mess"
python tracker.py add 30 transport "auto to market"
python tracker.py add 200 stationery "graph notebook" 2025-03-10
python tracker.py add 499 recharge "Jio 28 day plan"
```

### List Expenses

```bash
python tracker.py list                    # all expenses
python tracker.py list food               # filter by category
python tracker.py list food 2025-03       # filter by category and month
python tracker.py list 2025-03            # filter by month only
```

### View Summary

```bash
python tracker.py summary                 # overall summary
python tracker.py summary 2025-03         # summary for March 2025
```

Output looks like:
```
  Summary for 2025-03:

  Category             Amount    Share
  --------------------------------------
  food             Rs. 950.00    47.5%  #########
  transport        Rs. 480.00    24.0%  ####
  stationery       Rs. 350.00    17.5%  ###
  recharge         Rs. 220.00    11.0%  ##
  --------------------------------------
  Total            Rs.2000.00
```

### Set and Track Budget

```bash
python tracker.py budget 3000             # set budget for current month
python tracker.py budget 3000 2025-04     # set budget for a specific month
python tracker.py status                  # check current month's usage
python tracker.py status 2025-03          # check a specific month
```

Output looks like:
```
  Budget Status for 2025-03:
  Budget   : Rs.3000.00
  Spent    : Rs.2000.00 (66.7%)
  Remaining: Rs.1000.00
  [#############-------] 67%
  Status   : On track
```

### Delete an Entry

```bash
python tracker.py delete 4               # delete expense with ID 4
```

### Export to CSV

```bash
python tracker.py export
```

Saves to `data/expenses_export.csv`. Can be opened in Excel or Google Sheets.

### Help

```bash
python tracker.py help
```

---

## Categories

| Category      | Examples                                  |
|---------------|-------------------------------------------|
| food          | mess, canteen, restaurant, snacks         |
| transport     | auto, bus, train, cab                     |
| stationery    | notebook, pen, printing                   |
| entertainment | movie, gaming, OTT subscription           |
| medicine      | pharmacy, doctor                          |
| clothing      | clothes, shoes, laundry                   |
| recharge      | mobile recharge, internet pack            |
| other         | anything that doesn't fit above           |

---

## Project Structure

```
student-expense-tracker/
├── tracker.py          # Main program
├── test_tracker.py     # Unit tests
├── README.md
└── data/
    ├── expenses.json   # Auto-created on first use
    ├── budgets.json    # Auto-created when budget is set
    └── expenses_export.csv   # Created on export
```

---

## Data Format

Expenses are stored in `data/expenses.json`:

```json
[
  {
    "id": 1,
    "amount": 150.0,
    "category": "food",
    "note": "lunch at mess",
    "date": "2025-03-01"
  }
]
```

You can back this file up or move it between devices freely.

---

## Running Tests

```bash
python test_tracker.py
```

15 unit tests cover: adding valid/invalid entries, deletion, summary, load/save, and CSV export.

