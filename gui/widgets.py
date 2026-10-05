import tkinter as tk


BACKGROUND = "#F6F3E6"
WHITE = "#FFFFFF"
ORANGE = "#E5732F"
LIGHT_GRAY = "#F5F5F5"
TEXT_GRAY = "#777777"


class ResponsiveCategoryLegend:
    def __init__(self, parent, colors, category_manager):
        self.parent = parent
        self.colors = colors
        self.category_manager = category_manager

        self.frame = tk.Frame(
            parent,
            bg=WHITE
        )
        self.frame.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        self.frame.bind(
            "<Configure>",
            self._schedule_refresh
        )

        self._refresh_job = None

    def _schedule_refresh(self, event=None):
        if self._refresh_job is not None:
            self.frame.after_cancel(self._refresh_job)

        self._refresh_job = self.frame.after(
            80,
            self.refresh
        )

    def refresh(self):
        self._refresh_job = None

        for widget in self.frame.winfo_children():
            widget.destroy()

        categories = self.category_manager.get_categories()

        if not categories:
            return

        self.frame.update_idletasks()

        available_width = max(
            self.frame.winfo_width(),
            250
        )

        row = 0
        column = 0
        used_width = 0

        for index, category in enumerate(categories):
            color = self.colors[index]

            item = tk.Frame(
                self.frame,
                bg=WHITE
            )

            color_box = tk.Label(
                item,
                bg=color,
                width=2,
                height=1
            )
            color_box.pack(
                side=tk.LEFT,
                padx=(0, 4)
            )

            label = tk.Label(
                item,
                text=category,
                font=("Arial", 9),
                bg=WHITE
            )
            label.pack(side=tk.LEFT)

            item.update_idletasks()

            item_width = item.winfo_reqwidth() + 12

            if (
                column > 0
                and used_width + item_width > available_width
            ):
                row += 1
                column = 0
                used_width = 0

            item.grid(
                row=row,
                column=column,
                sticky="w",
                padx=(0, 12),
                pady=2
            )

            used_width += item_width
            column += 1

def center_window(window, parent=None):
    window.update_idletasks()

    width = window.winfo_width()
    height = window.winfo_height()

    if parent is not None:
        parent.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
    else:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

    x = max(x, 0)
    y = max(y, 0)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )

def create_button(
    parent,
    text,
    command,
    *,
    bold=True,
    padx=15,
    pady=8
):
    return tk.Button(
        parent,
        text=text,
        font=("Arial", 10, "bold" if bold else "normal"),
        bg=WHITE,
        bd=1,
        relief=tk.SOLID,
        padx=padx,
        pady=pady,
        command=command
    )


def create_card(parent, **pack_options):
    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=15,
        pady=15
    )

    card.pack(**pack_options)

    return card
