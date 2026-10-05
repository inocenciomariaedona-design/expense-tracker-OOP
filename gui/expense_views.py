import tkinter as tk
from datetime import datetime

from .transaction_row import TransactionRow


class ExpenseViews:
    VIEW_ALL = "All Expenses"
    VIEW_CATEGORY = "By Category"
    VIEW_DATE = "By Date"

    def __init__(
        self,
        parent,
        expense_manager,
        edit_callback,
        delete_callback
    ):
        self.parent = parent
        self.expense_manager = expense_manager
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback

        self.scroll_enabled = False
        self._resize_job = None
        self._wheel_bound = False

        self.card = tk.Frame(
            parent,
            bg="#FFFFFF",
            padx=15,
            pady=15
        )
        self.card.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        header = tk.Frame(
            self.card,
            bg="#FFFFFF"
        )
        header.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        header.columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="Recent transactions",
            font=("Arial", 11, "bold"),
            fg="#555555",
            bg="#FFFFFF"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.view_var = tk.StringVar(
            value=self.VIEW_ALL
        )

        self.view_menu = tk.OptionMenu(
            header,
            self.view_var,
            self.VIEW_ALL,
            self.VIEW_CATEGORY,
            self.VIEW_DATE,
            command=self._view_changed
        )
        self.view_menu.config(
            font=("Arial", 9),
            bg="#FFFFFF",
            activebackground="#FFFFFF"
        )
        self.view_menu.grid(
            row=0,
            column=1,
            sticky="e"
        )

        body = tk.Frame(
            self.card,
            bg="#FFFFFF"
        )
        body.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.canvas = tk.Canvas(
            body,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.scrollbar = tk.Scrollbar(
            body,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.container = tk.Frame(
            self.canvas,
            bg="#FFFFFF"
        )

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.container,
            anchor="nw"
        )

        self.container.bind(
            "<Configure>",
            self._on_container_configure
        )

        self.canvas.bind(
            "<Configure>",
            self._on_canvas_configure
        )

        self.canvas.bind(
            "<Enter>",
            self._bind_mousewheel
        )

        self.canvas.bind(
            "<Leave>",
            self._unbind_mousewheel
        )

    def _view_changed(self, value=None):
        self.refresh()

    def _on_container_configure(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )
        self._schedule_scroll_check()

    def _on_canvas_configure(self, event=None):
        self.canvas.itemconfigure(
            self.window_id,
            width=self.canvas.winfo_width()
        )
        self._schedule_scroll_check()

    def _schedule_scroll_check(self):
        if self._resize_job is not None:
            self.card.after_cancel(self._resize_job)

        self._resize_job = self.card.after(
            50,
            self._update_scroll_state
        )

    def _update_scroll_state(self):
        self._resize_job = None

        self.card.update_idletasks()
        self.canvas.update_idletasks()
        self.container.update_idletasks()

        content_height = self.container.winfo_reqheight()
        canvas_height = self.canvas.winfo_height()

        should_scroll = (
            content_height > canvas_height + 2
        )

        if should_scroll and not self.scroll_enabled:
            self.scrollbar.pack(
                side=tk.RIGHT,
                fill=tk.Y
            )
            self.scroll_enabled = True

        elif not should_scroll and self.scroll_enabled:
            self.scrollbar.pack_forget()
            self.scroll_enabled = False
            self.canvas.yview_moveto(0)

        if not should_scroll:
            self.canvas.yview_moveto(0)

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _bind_mousewheel(self, event=None):
        if self.scroll_enabled and not self._wheel_bound:
            self.canvas.bind_all(
                "<MouseWheel>",
                self._on_mousewheel
            )
            self._wheel_bound = True

    def _unbind_mousewheel(self, event=None):
        if self._wheel_bound:
            self.canvas.unbind_all(
                "<MouseWheel>"
            )
            self._wheel_bound = False

    def _on_mousewheel(self, event):
        if not self.scroll_enabled:
            return

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def refresh(self):
        self._unbind_mousewheel()

        for widget in self.container.winfo_children():
            widget.destroy()

        expenses = self.expense_manager.get_expenses()

        if not expenses:
            tk.Label(
                self.container,
                text="No transactions yet.",
                font=("Arial", 10),
                fg="#777777",
                bg="#FFFFFF"
            ).pack(
                anchor="w",
                pady=10
            )
            self._schedule_scroll_check()
            return

        view = self.view_var.get()

        if view == self.VIEW_CATEGORY:
            self._display_by_category()
        elif view == self.VIEW_DATE:
            self._display_by_date()
        else:
            self._display_all()

        self.canvas.yview_moveto(0)
        self._schedule_scroll_check()

    def _display_all(self):
        for index, expense in (
            self.expense_manager.get_expenses_sorted_by_date()
        ):
            TransactionRow(
                self.container,
                expense,
                index,
                self.edit_callback,
                self.delete_callback
            )

    def _display_by_category(self):
        grouped = (
            self.expense_manager
            .get_expenses_by_category()
        )

        for category, items in grouped.items():
            total = sum(
                expense.amount
                for _, expense in items
            )

            self._create_group_header(
                category,
                f"₱ {total:,.2f}"
            )

            for index, expense in items:
                TransactionRow(
                    self.container,
                    expense,
                    index,
                    self.edit_callback,
                    self.delete_callback
                )

    def _display_by_date(self):
        grouped = (
            self.expense_manager
            .get_expenses_by_date()
        )

        for date_text, items in grouped.items():
            total = sum(
                expense.amount
                for _, expense in items
            )

            formatted_date = self._format_date(date_text)

            self._create_group_header(
                formatted_date,
                f"₱ {total:,.2f}"
            )

            for index, expense in items:
                TransactionRow(
                    self.container,
                    expense,
                    index,
                    self.edit_callback,
                    self.delete_callback,
                    category_prefix=True
                )

    def _create_group_header(self, title, amount):
        frame = tk.Frame(
            self.container,
            bg="#FFFFFF"
        )
        frame.pack(
            fill=tk.X,
            pady=(8, 2)
        )

        frame.columnconfigure(0, weight=1)

        tk.Label(
            frame,
            text=title,
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        tk.Label(
            frame,
            text=amount,
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            anchor="e"
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        tk.Frame(
            self.container,
            height=1,
            bg="#E5E5E5"
        ).pack(
            fill=tk.X,
            pady=(2, 3)
        )

    @staticmethod
    def _format_date(date_text):
        try:
            return datetime.strptime(
                date_text,
                "%Y-%m-%d"
            ).strftime("%B %d, %Y")
        except (ValueError, TypeError):
            return date_text
