import tkinter as tk
from tkinter import messagebox

from date_picker import DatePicker
from .widgets import center_window


class ExpenseForm:
    def __init__(
        self,
        parent,
        category_manager,
        on_save,
        expense=None,
        index=None
    ):
        self.parent = parent
        self.category_manager = category_manager
        self.on_save = on_save
        self.expense = expense
        self.index = index

        self.is_edit = expense is not None

        self.window = tk.Toplevel(parent)
        self.window.title(
            "Edit Expense" if self.is_edit else "Add Expense"
        )
        self.window.geometry("400x400")
        self.window.configure(bg="#F6F3E6")
        self.window.resizable(False, False)

        center_window(
            self.window,
            self.parent
        )
        
        self.window.transient(parent)
        self.window.grab_set()

        self._build()

    def _build(self):
        title = (
            "Edit Expense"
            if self.is_edit
            else "Add Expense"
        )

        tk.Label(
            self.window,
            text=title,
            font=("Arial", 16, "bold"),
            bg="#F6F3E6"
        ).pack(pady=(20, 15))

        self.description_entry = self._create_entry(
            "Description"
        )

        self.amount_entry = self._create_entry(
            "Amount"
        )

        tk.Label(
            self.window,
            text="Category",
            bg="#F6F3E6",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=30
        )

        self.category_var = tk.StringVar()

        categories = (
            self.category_manager.get_categories()
        )

        if categories:
            self.category_var.set(
                self.expense.category
                if self.is_edit
                and self.expense.category in categories
                else categories[0]
            )

        self.category_menu = tk.OptionMenu(
            self.window,
            self.category_var,
            *categories
        )
        self.category_menu.config(
            font=("Arial", 10),
            bg="#FFFFFF"
        )
        self.category_menu.pack(
            fill=tk.X,
            padx=30,
            pady=(5, 15)
        )

        tk.Label(
            self.window,
            text="Date",
            bg="#F6F3E6",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=30
        )

        date_frame = tk.Frame(
            self.window,
            bg="#F6F3E6"
        )
        date_frame.pack(
            fill=tk.X,
            padx=30,
            pady=(5, 20)
        )

        self.date_entry = tk.Entry(
            date_frame,
            font=("Arial", 10)
        )
        self.date_entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        tk.Button(
            date_frame,
            text="Calendar",
            font=("Arial", 9),
            command=self.open_date_picker
        ).pack(
            side=tk.RIGHT,
            padx=(5, 0)
        )

        if self.is_edit:
            self.description_entry.insert(
                0,
                self.expense.description
            )
            self.amount_entry.insert(
                0,
                str(self.expense.amount)
            )
            self.date_entry.insert(
                0,
                self.expense.date
            )

        else:
            from datetime import date
            self.date_entry.insert(
                0,
                date.today().strftime("%Y-%m-%d")
            )

        button_text = (
            "Save Changes"
            if self.is_edit
            else "Save Expense"
        )

        tk.Button(
            self.window,
            text=button_text,
            font=("Arial", 10, "bold"),
            bg="#E5732F",
            fg="#FFFFFF",
            bd=0,
            padx=20,
            pady=8,
            command=self.save
        ).pack()

    def _create_entry(self, label_text):
        tk.Label(
            self.window,
            text=label_text,
            bg="#F6F3E6",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=30
        )

        entry = tk.Entry(
            self.window,
            font=("Arial", 10)
        )
        entry.pack(
            fill=tk.X,
            padx=30,
            pady=(5, 15)
        )

        return entry

    def open_date_picker(self):
        DatePicker(
            self.window,
            self.set_date,
            self.date_entry.get().strip()
        )

    def set_date(self, selected_date):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date)

    def save(self):
        description = (
            self.description_entry.get().strip()
        )
        amount_text = self.amount_entry.get().strip()
        category = self.category_var.get().strip()
        date_text = self.date_entry.get().strip()

        if not description:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a description.",
                parent=self.window
            )
            return

        if not amount_text:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an amount.",
                parent=self.window
            )
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Amount must be a number.",
                parent=self.window
            )
            return

        if amount <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Amount must be greater than zero.",
                parent=self.window
            )
            return

        if not category:
            messagebox.showerror(
                "Invalid Input",
                "Please select a category.",
                parent=self.window
            )
            return

        if not date_text:
            messagebox.showerror(
                "Invalid Input",
                "Please select a date.",
                parent=self.window
            )
            return

        from datetime import datetime, date

        try:
            selected = datetime.strptime(
                date_text,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Date must use YYYY-MM-DD format.",
                parent=self.window
            )
            return

        if selected > date.today():
            messagebox.showerror(
                "Invalid Input",
                "Future dates are not allowed.",
                parent=self.window
            )
            return

        self.on_save(
            amount,
            category,
            description,
            date_text,
            self.index
        )

        self.window.destroy()
