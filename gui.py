import tkinter as tk
from tkinter import messagebox, simpledialog

from expense import ExpenseManager
from category import CategoryManager


# ============================================================
# OOP DATA MANAGERS
# ============================================================

expense_manager = ExpenseManager()
category_manager = CategoryManager()


# ============================================================
# CATEGORY COLORS
# ============================================================

category_colors = [
    "#E5732F",
    "#5D9CEC",
    "#64F012",
    "#2B62D9",
    "#FF6384",
    "#D509F0",
    "#FF9F40",
    "#EAFA0E",
    "#36A2EB",
    "#4BC0C0",
    "#9966FF",
    "#FFCD56",
    "#FF8A65",
    "#66BB6A",
    "#AB47BC",
    "#26A69A",
    "#EC407A",
    "#5C6BC0",
    "#78909C"
]


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def calculate_total():
    """Calculates the total amount of all expenses."""

    return expense_manager.calculate_total()


def calculate_category_total(category):
    """Calculates the total spending for one category."""

    return expense_manager.calculate_category_total(category)


# ============================================================
# GUI UPDATE FUNCTIONS
# ============================================================

def refresh_gui():
    """Refreshes all information displayed in the GUI."""

    update_total()
    update_category_legend()
    update_category_bar()
    update_transactions()


def update_total():
    """Updates the total spending displayed on the screen."""

    total = calculate_total()

    label_amount.config(
        text=f"₱ {total:,.2f}"
    )


def update_category_legend():
    """Updates the category legend."""

    for widget in legend_frame.winfo_children():
        widget.destroy()

    categories = category_manager.get_categories()

    for index in range(len(categories)):

        color = category_colors[
            index % len(category_colors)
        ]

        color_box = tk.Label(
            legend_frame,
            bg=color,
            width=2,
            height=1
        )

        color_box.pack(
            side=tk.LEFT,
            padx=(0, 4)
        )

        category_label = tk.Label(
            legend_frame,
            text=categories[index],
            font=("Arial", 9),
            bg="#FFFFFF"
        )

        category_label.pack(
            side=tk.LEFT,
            padx=(0, 12)
        )


def update_category_bar():
    """Updates the category spending bar."""

    for widget in bar_container.winfo_children():
        widget.destroy()

    categories = category_manager.get_categories()
    total = calculate_total()

    if total == 0:
        return

    current_x = 0.0

    for index in range(len(categories)):

        category_total = calculate_category_total(
            categories[index]
        )

        segment_width = category_total / total

        if segment_width <= 0:
            continue

        color = category_colors[
            index % len(category_colors)
        ]

        segment = tk.Frame(
            bar_container,
            bg=color
        )

        segment.place(
            relx=current_x,
            rely=0,
            relwidth=segment_width,
            relheight=1.0
        )

        current_x += segment_width


def update_transactions():
    """Updates the Recent Transactions section."""

    for widget in transactions_container.winfo_children():
        widget.destroy()

    expenses = expense_manager.get_expenses()

    if len(expenses) == 0:

        empty_label = tk.Label(
            transactions_container,
            text="No transactions yet.",
            font=("Arial", 10),
            fg="#777777",
            bg="#FFFFFF"
        )

        empty_label.pack(
            anchor="w",
            pady=10
        )

        return

    for index, expense in enumerate(expenses):

        create_transaction(
            transactions_container,
            expense,
            index
        )


# ============================================================
# ADD EXPENSE
# ============================================================

def open_add_expense():
    """Opens the Add Expense window."""

    window = tk.Toplevel(root)

    window.title("Add Expense")
    window.geometry("400x400")
    window.configure(bg="#F6F3E6")
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="Add Expense",
        font=("Arial", 16, "bold"),
        bg="#F6F3E6"
    )

    title.pack(
        pady=(20, 15)
    )

    # Description

    tk.Label(
        window,
        text="Description",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    description_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )

    description_entry.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 15)
    )

    # Amount

    tk.Label(
        window,
        text="Amount",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    amount_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )

    amount_entry.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 15)
    )

    # Category

    tk.Label(
        window,
        text="Category",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    category_var = tk.StringVar()

    categories = category_manager.get_categories()

    if categories:
        category_var.set(categories[0])

    category_menu = tk.OptionMenu(
        window,
        category_var,
        *categories
    )

    category_menu.config(
        font=("Arial", 10),
        bg="#FFFFFF"
    )

    category_menu.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 15)
    )

    # Date

    tk.Label(
        window,
        text="Date",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    date_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )

    date_entry.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 20)
    )

    def save_expense():
        """Saves the new expense."""

        description = description_entry.get().strip()
        amount = amount_entry.get().strip()
        category = category_var.get()
        date = date_entry.get().strip()

        if not description:

            messagebox.showerror(
                "Invalid Input",
                "Please enter a description."
            )

            return

        if not amount:

            messagebox.showerror(
                "Invalid Input",
                "Please enter an amount."
            )

            return

        try:
            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Amount must be a number."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Invalid Input",
                "Amount must be greater than zero."
            )

            return

        if not category:

            messagebox.showerror(
                "Invalid Input",
                "Please select a category."
            )

            return

        if not date:

            messagebox.showerror(
                "Invalid Input",
                "Please enter a date."
            )

            return

        expense_manager.add_expense(
            amount,
            category,
            description,
            date
        )

        refresh_gui()

        window.destroy()

    save_button = tk.Button(
        window,
        text="Save Expense",
        font=("Arial", 10, "bold"),
        bg="#E5732F",
        fg="#FFFFFF",
        bd=0,
        padx=20,
        pady=8,
        command=save_expense
    )

    save_button.pack()


# ============================================================
# EDIT EXPENSE
# ============================================================

def open_edit_expense(index):
    """Opens the Edit Expense window."""

    expenses = expense_manager.get_expenses()

    if not (0 <= index < len(expenses)):
        return

    expense = expenses[index]

    window = tk.Toplevel(root)

    window.title("Edit Expense")
    window.geometry("400x400")
    window.configure(bg="#F6F3E6")
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="Edit Expense",
        font=("Arial", 16, "bold"),
        bg="#F6F3E6"
    )

    title.pack(
        pady=(20, 15)
    )

    # Description

    tk.Label(
        window,
        text="Description",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    description_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )

    description_entry.insert(
        0,
        expense.description
    )

    description_entry.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 15)
    )

    # Amount

    tk.Label(
        window,
        text="Amount",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    amount_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )

    amount_entry.insert(
        0,
        str(expense.amount)
    )

    amount_entry.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 15)
    )

    # Category

    tk.Label(
        window,
        text="Category",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    category_var = tk.StringVar()

    categories = category_manager.get_categories()

    category_var.set(
        expense.category
    )

    category_menu = tk.OptionMenu(
        window,
        category_var,
        *categories
    )

    category_menu.config(
        font=("Arial", 10),
        bg="#FFFFFF"
    )

    category_menu.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 15)
    )

    # Date

    tk.Label(
        window,
        text="Date",
        bg="#F6F3E6",
        font=("Arial", 10)
    ).pack(
        anchor="w",
        padx=30
    )

    date_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )

    date_entry.insert(
        0,
        expense.date
    )

    date_entry.pack(
        fill=tk.X,
        padx=30,
        pady=(5, 20)
    )

    def save_changes():
        """Saves the edited expense."""

        description = description_entry.get().strip()
        amount = amount_entry.get().strip()
        category = category_var.get()
        date = date_entry.get().strip()

        if not description:

            messagebox.showerror(
                "Invalid Input",
                "Please enter a description."
            )

            return

        try:
            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Amount must be a number."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Invalid Input",
                "Amount must be greater than zero."
            )

            return

        if not category:

            messagebox.showerror(
                "Invalid Input",
                "Please select a category."
            )

            return

        if not date:

            messagebox.showerror(
                "Invalid Input",
                "Please enter a date."
            )

            return

        expense_manager.edit_expense(
            index,
            amount,
            category,
            description,
            date
        )

        refresh_gui()

        window.destroy()

    save_button = tk.Button(
        window,
        text="Save Changes",
        font=("Arial", 10, "bold"),
        bg="#E5732F",
        fg="#FFFFFF",
        bd=0,
        padx=20,
        pady=8,
        command=save_changes
    )

    save_button.pack()


# ============================================================
# DELETE EXPENSE
# ============================================================

def delete_transaction(index):
    """Deletes an expense."""

    expenses = expense_manager.get_expenses()

    if not (0 <= index < len(expenses)):
        return

    expense = expenses[index]

    confirm = messagebox.askyesno(
        "Delete Expense",
        f"Delete '{expense.description}'?"
    )

    if confirm:

        expense_manager.delete_expense(index)

        refresh_gui()


# ============================================================
# CATEGORY MANAGEMENT
# ============================================================

def open_categories():
    """Opens the Category Management window."""

    window = tk.Toplevel(root)

    window.title("Categories")
    window.geometry("400x450")
    window.configure(bg="#F6F3E6")
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="Categories",
        font=("Arial", 16, "bold"),
        bg="#F6F3E6"
    )

    title.pack(
        pady=(20, 15)
    )

    category_listbox = tk.Listbox(
        window,
        font=("Arial", 10),
        height=12
    )

    category_listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=30
    )

    def refresh_category_list():

        category_listbox.delete(
            0,
            tk.END
        )

        for category in category_manager.get_categories():

            category_listbox.insert(
                tk.END,
                category
            )

    refresh_category_list()

    # --------------------------------------------------------
    # ADD CATEGORY
    # --------------------------------------------------------

    def add_new_category():

        category = tk.simpledialog.askstring(
            "Add Category",
            "Enter category name:",
            parent=window
        )

        if category is None:
            return

        if category_manager.add_category(category):

            refresh_category_list()
            refresh_gui()

        else:

            messagebox.showerror(
                "Invalid Category",
                "Category is empty or already exists."
            )

    # --------------------------------------------------------
    # EDIT CATEGORY
    # --------------------------------------------------------

    def edit_selected_category():

        selection = category_listbox.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a category first."
            )

            return

        index = selection[0]

        new_category = tk.simpledialog.askstring(
            "Edit Category",
            "Enter new category name:",
            parent=window
        )

        if new_category is None:
            return

        result = category_manager.edit_category(
            index,
            new_category
        )

        if result is None:

            messagebox.showerror(
                "Invalid Category",
                "Category is empty or already exists."
            )

            return

        old_category, new_category = result

        # Update existing expenses using the old category

        for expense in expense_manager.get_expenses():

            if expense.category == old_category:

                expense.category = new_category

        refresh_category_list()
        refresh_gui()

    # --------------------------------------------------------
    # DELETE CATEGORY
    # --------------------------------------------------------

    def delete_selected_category():

        selection = category_listbox.curselection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a category first."
            )

            return

        index = selection[0]

        categories = category_manager.get_categories()

        selected_category = categories[index]

        # Prevent deleting a category currently being used

        for expense in expense_manager.get_expenses():

            if expense.category == selected_category:

                messagebox.showerror(
                    "Cannot Delete",
                    "This category is being used by an expense."
                )

                return

        confirm = messagebox.askyesno(
            "Delete Category",
            f"Delete '{selected_category}'?"
        )

        if confirm:

            category_manager.delete_category(index)

            refresh_category_list()
            refresh_gui()

    # --------------------------------------------------------
    # CATEGORY BUTTONS
    # --------------------------------------------------------

    button_frame = tk.Frame(
        window,
        bg="#F6F3E6"
    )

    button_frame.pack(
        fill=tk.X,
        padx=30,
        pady=15
    )

    add_button = tk.Button(
        button_frame,
        text="Add",
        font=("Arial", 9, "bold"),
        command=add_new_category
    )

    add_button.pack(
        side=tk.LEFT,
        expand=True,
        fill=tk.X,
        padx=(0, 5)
    )

    edit_button = tk.Button(
        button_frame,
        text="Edit",
        font=("Arial", 9, "bold"),
        command=edit_selected_category
    )

    edit_button.pack(
        side=tk.LEFT,
        expand=True,
        fill=tk.X,
        padx=5
    )

    delete_button = tk.Button(
        button_frame,
        text="Delete",
        font=("Arial", 9, "bold"),
        command=delete_selected_category
    )

    delete_button.pack(
        side=tk.LEFT,
        expand=True,
        fill=tk.X,
        padx=(5, 0)
    )


# ============================================================
# HEADER
# ============================================================

def create_header(parent):
    """Creates the orange header and logo."""

    header = tk.Frame(
        parent,
        bg="#E5732F",
        height=60
    )

    header.pack(
        fill=tk.X
    )

    header.pack_propagate(False)

    logo_text = tk.Label(
        header,
        text="PERSONAL EXPENSE TRACKER",
        font=("Arial", 18, "bold"),
        bg="#E5732F",
        fg="#000000"
    )

    logo_text.pack(
        side=tk.LEFT,
        padx=20,
        pady=10
    )


# ============================================================
# TOTAL SPENDING CARD
# ============================================================

def create_total_card(parent):
    """Creates the total spending card."""

    global label_amount
    global legend_frame
    global bar_container

    card_total = tk.Frame(
        parent,
        bg="#FFFFFF",
        padx=15,
        pady=15
    )

    card_total.pack(
        fill=tk.X,
        pady=(0, 15)
    )

    label_title = tk.Label(
        card_total,
        text="Total spent this month",
        font=("Arial", 11),
        fg="#777777",
        bg="#FFFFFF"
    )

    label_title.pack(
        anchor="w"
    )

    label_amount = tk.Label(
        card_total,
        text="₱ 0.00",
        font=("Arial", 30, "bold"),
        bg="#FFFFFF"
    )

    label_amount.pack(
        anchor="w",
        pady=(0, 10)
    )

    # --------------------------------------------------------
    # CATEGORY LEGEND
    # --------------------------------------------------------

    legend_frame = tk.Frame(
        card_total,
        bg="#FFFFFF"
    )

    legend_frame.pack(
        fill=tk.X,
        pady=(0, 10)
    )

    # --------------------------------------------------------
    # CATEGORY BAR
    # --------------------------------------------------------

    bar_container = tk.Frame(
        card_total,
        height=12,
        bg="#E0E0E0"
    )

    bar_container.pack(
        fill=tk.X
    )

    bar_container.pack_propagate(False)


# ============================================================
# TRANSACTION ROW
# ============================================================

def create_transaction(parent, expense, index):
    """Creates one transaction row."""

    row = tk.Frame(
        parent,
        bg="#FFFFFF"
    )

    row.pack(
        fill=tk.X,
        pady=6
    )

    # --------------------------------------------------------
    # Transaction details
    # --------------------------------------------------------

    details = tk.Frame(
        row,
        bg="#FFFFFF"
    )

    details.pack(
        side=tk.LEFT
    )

    transaction_name = tk.Label(
        details,
        text=expense.description,
        font=("Arial", 10, "bold"),
        bg="#FFFFFF"
    )

    transaction_name.pack(
        anchor="w"
    )

    transaction_sub = tk.Label(
        details,
        text=f"{expense.category}  |  {expense.date}",
        font=("Arial", 8),
        fg="#777777",
        bg="#FFFFFF"
    )

    transaction_sub.pack(
        anchor="w"
    )

    # --------------------------------------------------------
    # Transaction amount and buttons
    # --------------------------------------------------------

    actions = tk.Frame(
        row,
        bg="#FFFFFF"
    )

    actions.pack(
        side=tk.RIGHT
    )

    amount = tk.Label(
        actions,
        text=f"- ₱ {expense.amount:,.2f}",
        font=("Arial", 10, "bold"),
        bg="#FFFFFF"
    )

    amount.pack(
        side=tk.LEFT,
        padx=(0, 6)
    )

    edit_button = tk.Button(
        actions,
        text="Edit",
        font=("Arial", 8),
        bd=1,
        relief=tk.SOLID,
        bg="#F5F5F5",
        command=lambda i=index: open_edit_expense(i)
    )

    edit_button.pack(
        side=tk.LEFT,
        padx=(0, 4)
    )

    delete_button = tk.Button(
        actions,
        text="Delete",
        font=("Arial", 8),
        bd=1,
        relief=tk.SOLID,
        bg="#F5F5F5",
        command=lambda i=index: delete_transaction(i)
    )

    delete_button.pack(
        side=tk.RIGHT
    )


# ============================================================
# RECENT TRANSACTIONS CARD
# ============================================================

def create_transactions_card(parent):
    """Creates the Recent Transactions section."""

    global transactions_container

    card_transactions = tk.Frame(
        parent,
        bg="#FFFFFF",
        padx=15,
        pady=15
    )

    card_transactions.pack(
        fill=tk.BOTH,
        expand=True
    )

    recent_label = tk.Label(
        card_transactions,
        text="Recent transactions",
        font=("Arial", 11, "bold"),
        fg="#555555",
        bg="#FFFFFF"
    )

    recent_label.pack(
        anchor="w",
        pady=(0, 10)
    )

    transactions_container = tk.Frame(
        card_transactions,
        bg="#FFFFFF"
    )

    transactions_container.pack(
        fill=tk.BOTH,
        expand=True
    )


# ============================================================
# ACTION BUTTONS
# ============================================================

def create_action_buttons(parent):
    """Creates the action buttons on the right side."""

    add_button = tk.Button(
        parent,
        text="+ Add expense",
        font=("Arial", 10, "bold"),
        bg="#FFFFFF",
        bd=1,
        relief=tk.SOLID,
        padx=15,
        pady=8,
        command=open_add_expense
    )

    add_button.pack(
        fill=tk.X,
        pady=(0, 10)
    )

    category_button = tk.Button(
        parent,
        text="Category",
        font=("Arial", 10, "bold"),
        bg="#FFFFFF",
        bd=1,
        relief=tk.SOLID,
        padx=15,
        pady=8,
        command=open_categories
    )

    category_button.pack(
        fill=tk.X
    )


# ============================================================
# MAIN CONTENT
# ============================================================

def create_main_content(parent):
    """Creates the main content area."""

    content = tk.Frame(
        parent,
        bg="#F6F3E6"
    )

    content.pack(
        fill=tk.BOTH,
        expand=True,
        padx=30,
        pady=20
    )

    # --------------------------------------------------------
    # Left column
    # --------------------------------------------------------

    left_column = tk.Frame(
        content,
        bg="#F6F3E6"
    )

    left_column.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True,
        padx=(0, 20)
    )

    # --------------------------------------------------------
    # Right column
    # --------------------------------------------------------

    right_column = tk.Frame(
        content,
        bg="#F6F3E6"
    )

    right_column.pack(
        side=tk.RIGHT,
        fill=tk.Y,
        anchor="n"
    )

    # --------------------------------------------------------
    # Create sections
    # --------------------------------------------------------

    create_total_card(left_column)

    create_transactions_card(left_column)

    create_action_buttons(right_column)


# ============================================================
# MAIN GUI FUNCTION
# ============================================================

def create_gui():
    """Creates and starts the Expense Tracker GUI."""

    global root

    root = tk.Tk()

    root.title("Expense Tracker")

    root.geometry("850x600")

    root.configure(
        bg="#F6F3E6"
    )

    create_header(root)

    create_main_content(root)

    refresh_gui()

    root.mainloop()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    create_gui()