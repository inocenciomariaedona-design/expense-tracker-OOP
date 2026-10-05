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
        expense = Expense(
            amount,
            category,
            description,
            date
        )

        self.expenses.append(expense)

    def edit_expense(self, index, amount, category, description, date):
        if 0 <= index < len(self.expenses):
            self.expenses[index] = Expense(
                amount,
                category,
                description,
                date
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
        total = 0

        for expense in self.expenses:
            total += expense.amount

        return total

    def calculate_category_total(self, category):
        total = 0

        for expense in self.expenses:
            if expense.category == category:
                total += expense.amount

        return total
