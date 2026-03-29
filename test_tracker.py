"""
Unit tests for Student Expense Tracker
Author: Jishant Tanwar
Reg. No.: 25BHI10093
"""

import os
import sys
import json
import unittest
import tempfile
import shutil

# Point DATA_FILE to a temp directory during tests
TEST_DIR = tempfile.mkdtemp()
os.environ["EXPENSE_TEST_MODE"] = "1"

# Patch the DATA_FILE path before importing tracker
import importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tracker
tracker.DATA_FILE = os.path.join(TEST_DIR, "expenses.json")

BUDGET_FILE = os.path.join(TEST_DIR, "budgets.json")


class TestAddExpense(unittest.TestCase):

    def setUp(self):
        # Clean slate before each test
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)

    def test_add_valid_expense(self):
        tracker.add_expense(100, "food", "biryani", "2025-03-01")
        data = tracker.load_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["amount"], 100.0)
        self.assertEqual(data[0]["category"], "food")
        self.assertEqual(data[0]["note"], "biryani")

    def test_add_invalid_category(self, capsys=None):
        tracker.add_expense(100, "aliens", "snacks", "2025-03-01")
        data = tracker.load_data()
        self.assertEqual(len(data), 0)

    def test_add_zero_amount(self):
        tracker.add_expense(0, "food", "free food", "2025-03-01")
        data = tracker.load_data()
        self.assertEqual(len(data), 0)

    def test_add_negative_amount(self):
        tracker.add_expense(-50, "food", "", "2025-03-01")
        data = tracker.load_data()
        self.assertEqual(len(data), 0)

    def test_add_multiple_expenses(self):
        tracker.add_expense(150, "food", "lunch", "2025-03-01")
        tracker.add_expense(30, "transport", "auto", "2025-03-02")
        tracker.add_expense(200, "stationery", "notebook", "2025-03-03")
        data = tracker.load_data()
        self.assertEqual(len(data), 3)

    def test_ids_are_unique(self):
        tracker.add_expense(100, "food", "", "2025-03-01")
        tracker.add_expense(200, "food", "", "2025-03-02")
        tracker.add_expense(300, "food", "", "2025-03-03")
        data = tracker.load_data()
        ids = [e["id"] for e in data]
        self.assertEqual(len(ids), len(set(ids)))


class TestDeleteExpense(unittest.TestCase):

    def setUp(self):
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)
        tracker.add_expense(100, "food", "lunch", "2025-03-01")
        tracker.add_expense(200, "transport", "uber", "2025-03-02")

    def test_delete_valid_id(self):
        data = tracker.load_data()
        first_id = data[0]["id"]
        tracker.delete_expense(first_id)
        data = tracker.load_data()
        self.assertEqual(len(data), 1)

    def test_delete_nonexistent_id(self):
        tracker.delete_expense(9999)
        data = tracker.load_data()
        self.assertEqual(len(data), 2)


class TestSummary(unittest.TestCase):

    def setUp(self):
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)
        tracker.add_expense(100, "food", "lunch", "2025-03-01")
        tracker.add_expense(50, "food", "snacks", "2025-03-02")
        tracker.add_expense(200, "transport", "bus pass", "2025-03-05")

    def test_summary_runs_without_crash(self):
        try:
            tracker.show_summary("2025-03")
        except Exception as e:
            self.fail(f"show_summary raised an exception: {e}")

    def test_summary_no_crash_empty(self):
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)
        try:
            tracker.show_summary()
        except Exception as e:
            self.fail(f"show_summary on empty data raised: {e}")


class TestLoadSave(unittest.TestCase):

    def setUp(self):
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)

    def test_load_empty(self):
        data = tracker.load_data()
        self.assertEqual(data, [])

    def test_save_and_load(self):
        sample = [{"id": 1, "amount": 50.0, "category": "food", "note": "test", "date": "2025-03-01"}]
        tracker.save_data(sample)
        loaded = tracker.load_data()
        self.assertEqual(loaded, sample)

    def test_load_invalid_json(self):
        os.makedirs(os.path.dirname(tracker.DATA_FILE), exist_ok=True)
        with open(tracker.DATA_FILE, "w") as f:
            f.write("this is not json {{{")
        data = tracker.load_data()
        self.assertEqual(data, [])


class TestExport(unittest.TestCase):

    def setUp(self):
        if os.path.exists(tracker.DATA_FILE):
            os.remove(tracker.DATA_FILE)
        tracker.add_expense(100, "food", "breakfast", "2025-03-01")
        tracker.add_expense(200, "recharge", "jio plan", "2025-03-03")

    def test_export_csv_creates_file(self):
        output = os.path.join(TEST_DIR, "test_export.csv")
        tracker.export_csv(output)
        self.assertTrue(os.path.exists(output))

    def test_export_csv_has_correct_rows(self):
        import csv
        output = os.path.join(TEST_DIR, "test_export2.csv")
        tracker.export_csv(output)
        with open(output, "r") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 2)


def teardown_module():
    shutil.rmtree(TEST_DIR, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)