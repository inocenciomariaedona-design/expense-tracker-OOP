import tkinter as tk
from tkinter import messagebox, simpledialog
from .widgets import center_window


class CategoryManagerUI:
    def __init__(
        self,
        parent,
        category_manager,
        expense_manager,
        on_refresh
    ):
        self.parent = parent
        self.category_manager = category_manager
        self.expense_manager = expense_manager
        self.on_refresh = on_refresh

        self.window = tk.Toplevel(parent)
        self.window.title("Categories")
        self.window.geometry("400x450")
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
        tk.Label(
            self.window,
            text="Categories",
            font=("Arial", 16, "bold"),
            bg="#F6F3E6"
        ).pack(pady=(20, 15))

        self.category_listbox = tk.Listbox(
            self.window,
            font=("Arial", 10),
            height=12
        )
        self.category_listbox.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30
        )

        self.status_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 8),
            fg="#777777",
            bg="#F6F3E6"
        )
        self.status_label.pack(
            anchor="w",
            padx=30,
            pady=(8, 0)
        )

        self._refresh_list()

        button_frame = tk.Frame(
            self.window,
            bg="#F6F3E6"
        )
        button_frame.pack(
            fill=tk.X,
            padx=30,
            pady=15
        )

        tk.Button(
            button_frame,
            text="Add",
            font=("Arial", 9, "bold"),
            command=self.add_category
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=(0, 5)
        )

        tk.Button(
            button_frame,
            text="Edit",
            font=("Arial", 9, "bold"),
            command=self.edit_category
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Delete",
            font=("Arial", 9, "bold"),
            command=self.delete_category
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=(5, 0)
        )

    def _refresh_list(self):
        self.category_listbox.delete(
            0,
            tk.END
        )

        for category in (
            self.category_manager.get_categories()
        ):
            self.category_listbox.insert(
                tk.END,
                category
            )

        remaining = (
            self.category_manager
            .get_remaining_slots()
        )

        self.status_label.config(
            text=f"{remaining} category slot(s) remaining."
        )

    def add_category(self):
        if not self.category_manager.can_add_category():
            messagebox.showerror(
                "Category Limit",
                "The maximum number of categories has been reached.",
                parent=self.window
            )
            return

        category = simpledialog.askstring(
            "Add Category",
            "Enter category name:",
            parent=self.window
        )

        if category is None:
            return

        if self.category_manager.add_category(category):
            self._refresh_list()
            self.on_refresh()
        else:
            messagebox.showerror(
                "Invalid Category",
                "Category is empty or already exists.",
                parent=self.window
            )

    def edit_category(self):
        selection = (
            self.category_listbox.curselection()
        )

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a category first.",
                parent=self.window
            )
            return

        index = selection[0]

        new_category = simpledialog.askstring(
            "Edit Category",
            "Enter new category name:",
            parent=self.window
        )

        if new_category is None:
            return

        result = self.category_manager.edit_category(
            index,
            new_category
        )

        if result is None:
            messagebox.showerror(
                "Invalid Category",
                "Category is empty or already exists.",
                parent=self.window
            )
            return

        old_category, new_category = result

        self.expense_manager.update_category_name(
            old_category,
            new_category
        )

        self._refresh_list()
        self.on_refresh()

    def delete_category(self):
        selection = (
            self.category_listbox.curselection()
        )

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a category first.",
                parent=self.window
            )
            return

        index = selection[0]
        category = (
            self.category_manager
            .get_categories()[index]
        )

        if self.expense_manager.is_category_used(
            category
        ):
            messagebox.showerror(
                "Cannot Delete",
                "This category is being used by an expense.",
                parent=self.window
            )
            return

        confirm = messagebox.askyesno(
            "Delete Category",
            f"Delete '{category}'?",
            parent=self.window
        )

        if not confirm:
            return

        self.category_manager.delete_category(index)

        self._refresh_list()
        self.on_refresh()
