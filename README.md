# expense-tracker

A Personal Expense Tracker developed in Python using the **Object-Oriented Programming (OOP) paradigm**.

This project was originally developed as a procedural expense tracker and was then converted into an object-oriented version to demonstrate how the same application can be structured using classes and objects.

## Branches

### `main` — B1: OOP Conversion

The `main` branch contains the working object-oriented conversion of the original procedural expense tracker.

It introduces classes such as:

- `Expense`
- `ExpenseManager`
- `CategoryManager`

The main branch preserves the original functionality of the tracker while moving the expense and category data and their related operations into classes.

The B1 implementation has also been updated and corrected through subsequent pushes to the `main` branch.

### `oop-refactor` — B2: Expanded OOP Version

The `oop-refactor` branch was created to further expand the features of the tracker and to portray the OOP paradigm more extensively.

In addition to the functionality available in `main`, this branch includes:

- Calendar-based date selection
- Prevention of future expense dates
- Multiple expense viewing modes:
  - All Expenses
  - By Category
  - By Date
- Category limit based on the available category colors
- Responsive window layout
- Responsive category legend
- Scrollable expense list when content exceeds the available space
- Separate classes for major GUI components
- Improved separation of responsibilities between the data layer and interface

The refactored version moves more of the application's behavior into classes, including the main application window, expense form, expense views, category manager interface, transaction rows, date picker, and responsive category legend.

This branch was created as a further development of the OOP implementation and serves as a stronger demonstration of object-oriented design through **encapsulation, composition, modularity, and separation of responsibilities**.

## Running the Program

Install Python 3 and run the application from the selected branch.

### Main branch

```bash
python gui.py
