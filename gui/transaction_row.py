import tkinter as tk


class TransactionRow:
    def __init__(
        self,
        parent,
        expense,
        index,
        edit_callback,
        delete_callback,
        category_prefix=True
    ):
        self.parent = parent
        self.expense = expense
        self.index = index

        self.row = tk.Frame(
            parent,
            bg="#FFFFFF"
        )
        self.row.pack(
            fill=tk.X,
            pady=6
        )

        self.row.columnconfigure(0, weight=1)

        details = tk.Frame(
            self.row,
            bg="#FFFFFF"
        )
        details.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        details.columnconfigure(0, weight=1)

        tk.Label(
            details,
            text=expense.description,
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        if category_prefix:
            subtitle = (
                f"{expense.category}  |  {expense.date}"
            )
        else:
            subtitle = expense.date

        tk.Label(
            details,
            text=subtitle,
            font=("Arial", 8),
            fg="#777777",
            bg="#FFFFFF",
            anchor="w"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        actions = tk.Frame(
            self.row,
            bg="#FFFFFF"
        )
        actions.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(10, 0)
        )

        tk.Label(
            actions,
            text=f"- ₱ {expense.amount:,.2f}",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF"
        ).pack(
            side=tk.LEFT,
            padx=(0, 6)
        )

        tk.Button(
            actions,
            text="Edit",
            font=("Arial", 8),
            bd=1,
            relief=tk.SOLID,
            bg="#F5F5F5",
            command=lambda: edit_callback(self.index)
        ).pack(
            side=tk.LEFT,
            padx=(0, 4)
        )

        tk.Button(
            actions,
            text="Delete",
            font=("Arial", 8),
            bd=1,
            relief=tk.SOLID,
            bg="#F5F5F5",
            command=lambda: delete_callback(self.index)
        ).pack(side=tk.LEFT)
