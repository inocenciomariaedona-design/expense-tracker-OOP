import tkinter as tk
from tkinter import messagebox

from expense import ExpenseManager
from category import CategoryManager
from category_colors import CATEGORY_COLORS, MAX_CATEGORIES

from .widgets import (
    BACKGROUND,
    WHITE,
    ORANGE,
    ResponsiveCategoryLegend,
    create_button
)
from .expense_form import ExpenseForm
from .expense_views import ExpenseViews
from .category_manager_ui import CategoryManagerUI


class ExpenseTrackerApp:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Expense Tracker")
        self.root.geometry("850x600")
        self.root.minsize(700, 500)
        self.root.configure(bg=BACKGROUND)

        self.expense_manager = ExpenseManager()
        self.category_manager = CategoryManager(
            MAX_CATEGORIES
        )

        self.total_amount_label = None
        self.bar_container = None
        self.legend = None
        self.expense_views = None

        self._build()

    def _build(self):
        self._create_header()
        self._create_main_content()

        self.refresh()

    def _create_header(self):
        header = tk.Frame(
            self.root,
            bg=ORANGE,
            height=60
        )

        header.pack(
            fill=tk.X
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="PERSONAL EXPENSE TRACKER",
            font=("Arial", 18, "bold"),
            bg=ORANGE,
            fg="#000000"
        ).pack(
            side=tk.LEFT,
            padx=20,
            pady=10
        )

    def _create_main_content(self):
        self.content = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        self.content.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=20
        )

        # Left side expands with the window
        self.content.grid_columnconfigure(
            0,
            weight=1
        )

        # Right side stays at its fixed button width
        self.content.grid_columnconfigure(
            1,
            weight=0
        )

        self.content.grid_rowconfigure(
            0,
            weight=1
        )

        # -------------------------------------------------
        # LEFT COLUMN
        # -------------------------------------------------

        self.left_column = tk.Frame(
            self.content,
            bg=BACKGROUND
        )

        self.left_column.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 20)
        )

        # IMPORTANT:
        # Allows the white cards inside the left column
        # to expand horizontally with the window.
        self.left_column.grid_columnconfigure(
            0,
            weight=1
        )

        # The recent-transactions section expands vertically.
        self.left_column.grid_rowconfigure(
            1,
            weight=1
        )

        # -------------------------------------------------
        # RIGHT COLUMN
        # -------------------------------------------------

        self.right_column = tk.Frame(
            self.content,
            bg=BACKGROUND,
            width=150
        )

        self.right_column.grid(
            row=0,
            column=1,
            sticky="n"
        )

        self.right_column.grid_propagate(False)

        # -------------------------------------------------
        # COMPONENTS
        # -------------------------------------------------

        self._create_total_card()
        self._create_action_buttons()

        self.expense_views = ExpenseViews(
            self.left_column,
            self.expense_manager,
            self.open_edit_expense,
            self.delete_transaction
        )

        self.left_column.grid_rowconfigure(
            1,
            weight=1
        )

        self.root.bind(
            "<Configure>",
            self._on_window_resize
        )

    def _create_total_card(self):
        card = tk.Frame(
            self.left_column,
            bg=WHITE,
            padx=15,
            pady=15
        )

        card.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.total_card = card

        tk.Label(
            card,
            text="Total spent this month",
            font=("Arial", 11),
            fg="#777777",
            bg=WHITE
        ).pack(
            anchor="w"
        )

        self.total_amount_label = tk.Label(
            card,
            text="₱ 0.00",
            font=("Arial", 30, "bold"),
            bg=WHITE
        )

        self.total_amount_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        self.legend = ResponsiveCategoryLegend(
            card,
            CATEGORY_COLORS,
            self.category_manager
        )

        self.bar_container = tk.Frame(
            card,
            height=12,
            bg="#E0E0E0"
        )

        self.bar_container.pack(
            fill=tk.X
        )

        self.bar_container.pack_propagate(False)

    def _create_action_buttons(self):
        create_button(
            self.right_column,
            "+ Add expense",
            self.open_add_expense
        ).pack(
            fill=tk.X,
            pady=(0, 10)
        )

        create_button(
            self.right_column,
            "Category",
            self.open_categories
        ).pack(
            fill=tk.X
        )

    def _on_window_resize(self, event):
        # Only respond to the main application window.
        if event.widget != self.root:
            return

        width = self.root.winfo_width()

        if width < 760:
            self.right_column.config(
                width=130
            )

            self.content.config(
                padx=20
            )

        else:
            self.right_column.config(
                width=150
            )

            self.content.config(
                padx=30
            )

    def refresh(self):
        self._update_total()
        self._update_category_legend()
        self._update_category_bar()

        if self.expense_views is not None:
            self.expense_views.refresh()

    def _update_total(self):
        total = self.expense_manager.calculate_total()

        self.total_amount_label.config(
            text=f"₱ {total:,.2f}"
        )

    def _update_category_legend(self):
        self.legend.refresh()

    def _update_category_bar(self):
        for widget in (
            self.bar_container.winfo_children()
        ):
            widget.destroy()

        total = self.expense_manager.calculate_total()

        if total <= 0:
            return

        current_x = 0.0

        for index, category in enumerate(
            self.category_manager.get_categories()
        ):
            category_total = (
                self.expense_manager
                .calculate_category_total(category)
            )

            if category_total <= 0:
                continue

            segment_width = (
                category_total / total
            )

            segment = tk.Frame(
                self.bar_container,
                bg=CATEGORY_COLORS[index]
            )

            segment.place(
                relx=current_x,
                rely=0,
                relwidth=segment_width,
                relheight=1.0
            )

            current_x += segment_width

    def open_add_expense(self):
        ExpenseForm(
            self.root,
            self.category_manager,
            self._save_expense
        )

    def open_edit_expense(self, index):
        expenses = self.expense_manager.get_expenses()

        if not (0 <= index < len(expenses)):
            return

        ExpenseForm(
            self.root,
            self.category_manager,
            self._save_expense,
            expense=expenses[index],
            index=index
        )

    def _save_expense(
        self,
        amount,
        category,
        description,
        date_text,
        index
    ):
        if index is None:
            self.expense_manager.add_expense(
                amount,
                category,
                description,
                date_text
            )

        else:
            self.expense_manager.edit_expense(
                index,
                amount,
                category,
                description,
                date_text
            )

        self.refresh()

    def delete_transaction(self, index):
        expenses = self.expense_manager.get_expenses()

        if not (0 <= index < len(expenses)):
            return

        expense = expenses[index]

        confirm = messagebox.askyesno(
            "Delete Expense",
            f"Delete '{expense.description}'?",
            parent=self.root
        )

        if confirm:
            self.expense_manager.delete_expense(
                index
            )

            self.refresh()

    def open_categories(self):
        CategoryManagerUI(
            self.root,
            self.category_manager,
            self.expense_manager,
            self.refresh
        )

    def run(self):
        self.root.mainloop()