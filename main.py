from expense import ExpenseManager
from category import CategoryManager


def main():
    expense_manager = ExpenseManager()
    category_manager = CategoryManager()

    print("Expense Tracker")
    print("----------------")

    expense_manager.add_expense(
        180,
        "Food",
        "Lunch",
        "09/23/2026"
    )

    print("\nRecent Transactions:")

    for expense in expense_manager.get_expenses():
        print(
            expense.description,
            "- ₱",
            expense.amount
        )

    print(
        "\nTotal spent: ₱",
        expense_manager.calculate_total()
    )

    print("\nCategories:")
    print(category_manager.get_categories())


if __name__ == "__main__":
    main()