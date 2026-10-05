# Personal Expense Tracker - OOP

Run the application with:

```bash
python app.py
```

Structure:
- `expense.py` - expense model and expense operations
- `category.py` - category operations and category limit
- `category_colors.py` - category colors and maximum category count
- `date_picker.py` - calendar date picker with future-date restriction
- `gui/main_window.py` - main application window
- `gui/expense_form.py` - add/edit expense form
- `gui/expense_views.py` - all/category/date expense views and conditional scrolling
- `gui/transaction_row.py` - individual transaction row
- `gui/category_manager_ui.py` - category management window
- `gui/widgets.py` - reusable GUI components

The expense list only becomes scrollable when its content is taller than the available area.
