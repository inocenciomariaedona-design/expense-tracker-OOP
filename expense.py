from collections import defaultdict
from datetime import datetime


class Expense:
    def __init__(self, amount, category, description, date):
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date


class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, description, date):
        self.expenses.append(
            Expense(amount, category, description, date)
        )

    def edit_expense(self, index, amount, category, description, date):
        if 0 <= index < len(self.expenses):
            self.expenses[index] = Expense(
                amount, category, description, date
            )
            return True
        return False

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            self.expenses.pop(index)
            return True
        return False

    def get_expenses(self):
        return self.expenses

    def calculate_total(self):
        return sum(expense.amount for expense in self.expenses)

    def calculate_category_total(self, category):
        return sum(
            expense.amount
            for expense in self.expenses
            if expense.category == category
        )

    def update_category_name(self, old_category, new_category):
        for expense in self.expenses:
            if expense.category == old_category:
                expense.category = new_category

    def is_category_used(self, category):
        return any(
            expense.category == category
            for expense in self.expenses
        )

    def get_expenses_sorted_by_date(self):
        indexed = list(enumerate(self.expenses))
        indexed.sort(
            key=lambda item: self._date_sort_key(item[1].date),
            reverse=True
        )
        return indexed

    def get_expenses_by_category(self):
        grouped = defaultdict(list)

        for index, expense in enumerate(self.expenses):
            grouped[expense.category].append((index, expense))

        for category in grouped:
            grouped[category].sort(
                key=lambda item: self._date_sort_key(item[1].date),
                reverse=True
            )

        return dict(
            sorted(
                grouped.items(),
                key=lambda item: item[0].lower()
            )
        )

    def get_expenses_by_date(self):
        grouped = defaultdict(list)

        for index, expense in enumerate(self.expenses):
            grouped[expense.date].append((index, expense))

        for date_value in grouped:
            grouped[date_value].sort(
                key=lambda item: item[1].description.lower()
            )

        sorted_dates = sorted(
            grouped.keys(),
            key=self._date_sort_key,
            reverse=True
        )

        return {
            date_value: grouped[date_value]
            for date_value in sorted_dates
        }

    @staticmethod
    def _date_sort_key(date_text):
        try:
            return datetime.strptime(date_text, "%Y-%m-%d")
        except (ValueError, TypeError):
            return datetime.min
