# ai-ml_project
# Student Expense Tracker
A command-line tool built in Python to help college students track daily expenses, set monthly budgets, understand spending patterns, and use basic AI/ML techniques to predict and analyze financial behaviour.

**Author:** Jishant Tanwar  
**Reg. No.:** 25BHI10093  
---
## Why I Built This

Living in a hostel on a fixed monthly allowance, I kept running out of money before the month ended and had no idea where it was all going. I built this tool to log expenses quickly, categorize them, check how much budget is left — and eventually added ML features to predict next month's spending and understand my spending patterns better.
---

## Features

- Add, list, and delete expense entries
- Organize spending into 8 categories (food, transport, stationery, etc.)
- Monthly budget tracking with a visual usage bar
- Category-wise summary with percentage breakdown
- Filter expenses by category or month
- Export all data to CSV for use in Excel or Google Sheets
- All data stored locally as JSON — no cloud, no account needed

**AI/ML Features (implemented from scratch using NumPy):**
- Predict next month's total spend using Linear Regression with gradient descent
- Cluster daily spending into Low / Moderate / High patterns using K-Means
- Auto-suggest expense category from a written note using a Keyword Classifier

---

## Requirements

- Python 3.7 or above
- NumPy (only required for the AI/ML commands)

```bash
pip install numpy
```

---
## Setup

```bash
git clone https://github.com/jishanttanwar/student-expense-tracker.git
cd student-expense-tracker
pip install numpy
```
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
python tracker.py summary
python tracker.py summary 2025-03
```

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

### Budget and Status

```bash
python tracker.py budget 3000             # set budget for current month
python tracker.py budget 3000 2025-04     # set budget for a specific month
python tracker.py status                  # check current month usage
python tracker.py status 2025-03          # check a specific month
```

### Delete and Export

```bash
python tracker.py delete 4               # delete by ID
python tracker.py export                 # export to data/expenses_export.csv
```

---

## AI/ML Commands

### Predict Next Month's Spending

```bash
python tracker.py predict
```

Trains a **Linear Regression** model using gradient descent on your past monthly spending totals. Outputs the model equation, R² score, and a spending forecast.

```
  Spending Trend (Linear Regression)
  --------------------------------------------
  Month          Actual Spend
  --------------------------------------------
  2025-01      Rs.    1499.00
  2025-02      Rs.    1539.00
  2025-03      Rs.    1629.00
  --------------------------------------------

  Model: spend = 65.0 x month_no + 1425.67
  R² Score : 0.953  (good fit)

  Predicted spend for 2025-04: Rs.1685.67
```

Requires at least 2 months of data.

### Cluster Spending Days

```bash
python tracker.py cluster
```

Applies **K-Means Clustering** (k=3) to group daily spending totals into Low, Moderate, and High Spend days. Shows day counts and your dominant pattern.

```
  Spending Pattern Clusters (K-Means, k=3)
  Days analyzed: 18
  --------------------------------------------
  Low Spend          Avg Rs.  127.00   10 days  ##########
  Moderate Spend     Avg Rs.  325.00    4 days  ####
  High Spend         Avg Rs.  524.25    4 days  ####
  --------------------------------------------
  Your dominant pattern : Low Spend (avg Rs.127.00/day)
```

Requires at least 3 days of data.

### Classify a Note into a Category

```bash
python tracker.py classify "biryani at mess"
python tracker.py classify "jio recharge 28 day plan"
```

Uses a **bag-of-words keyword classifier** to suggest the most likely expense category from a note, along with confidence scores.

```
  Category Classifier
  Note       : "biryani at mess with friends"
  Prediction : food  (confidence: 62%)
  All scores :
    food              62.5%  ############
    entertainment     12.5%  ##
    stationery        12.5%  ##
    recharge          12.5%  ##
```

---

## AI/ML Implementation Details

All algorithms are written from scratch — no scikit-learn or any ML library.

| Command | Algorithm | Concepts Used |
|---|---|---|
| `predict` | Linear Regression | Gradient descent, MSE loss, R² score, feature normalization |
| `cluster` | K-Means (k=3) | Centroid init, assign step, update step, convergence check |
| `classify` | Keyword Classifier | Bag-of-words, weighted scoring, confidence normalization |

---

## Project Structure

```
student-expense-tracker/
├── tracker.py          # Main program and CLI dispatcher
├── ml_insights.py      # AI/ML module (Linear Regression, K-Means, Classifier)
├── test_tracker.py     # 15 unit tests using unittest
├── README.md
└── data/
    ├── expenses.json         # Auto-created on first use
    ├── budgets.json          # Auto-created when budget is set
    └── expenses_export.csv   # Created when export is run
```

---

## Data Format

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

---

## Running Tests

```bash
python test_tracker.py
```

15 unit tests cover: adding valid/invalid entries, deletion, summary, load/save, and CSV export.

---

