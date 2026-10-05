import calendar
import tkinter as tk
from datetime import date
from gui.widgets import center_window


class DatePicker:
    def __init__(self, parent, callback, selected_date=None):
        self.parent = parent
        self.callback = callback
        self.today = date.today()

        parsed = self._parse_date(selected_date)
        self.selected_date = parsed or self.today

        if self.selected_date > self.today:
            self.selected_date = self.today

        self.current_year = self.selected_date.year
        self.current_month = self.selected_date.month

        self.window = tk.Toplevel(parent)
        self.window.title("Select Date")
        self.window.geometry("320x330")
        self.window.configure(bg="#F6F3E6")
        self.window.resizable(False, False)

        center_window(
            self.window,
            self.parent
        )

        self.window.transient(parent)
        self.window.grab_set()

        self.create_widgets()
        self.update_calendar()

    def _parse_date(self, date_text):
        if not date_text:
            return None

        try:
            year, month, day = map(int, date_text.split("-"))
            return date(year, month, day)
        except (ValueError, AttributeError):
            return None

    def create_widgets(self):
        tk.Label(
            self.window,
            text="Select Date",
            font=("Arial", 16, "bold"),
            bg="#F6F3E6"
        ).pack(pady=(15, 10))

        navigation = tk.Frame(
            self.window,
            bg="#F6F3E6"
        )
        navigation.pack(fill=tk.X, padx=20)

        self.previous_button = tk.Button(
            navigation,
            text="<",
            font=("Arial", 10, "bold"),
            width=4,
            command=self.previous_month
        )
        self.previous_button.pack(side=tk.LEFT)

        self.month_label = tk.Label(
            navigation,
            text="",
            font=("Arial", 11, "bold"),
            bg="#F6F3E6"
        )
        self.month_label.pack(
            side=tk.LEFT,
            expand=True
        )

        self.next_button = tk.Button(
            navigation,
            text=">",
            font=("Arial", 10, "bold"),
            width=4,
            command=self.next_month
        )
        self.next_button.pack(side=tk.RIGHT)

        self.calendar_frame = tk.Frame(
            self.window,
            bg="#F6F3E6"
        )
        self.calendar_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=10
        )

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(
            text=f"{calendar.month_name[self.current_month]} "
                 f"{self.current_year}"
        )

        weekdays = [
            "Mon", "Tue", "Wed",
            "Thu", "Fri", "Sat", "Sun"
        ]

        for column, weekday in enumerate(weekdays):
            tk.Label(
                self.calendar_frame,
                text=weekday,
                font=("Arial", 8, "bold"),
                bg="#F6F3E6"
            ).grid(
                row=0,
                column=column,
                padx=2,
                pady=2
            )

        month_calendar = calendar.monthcalendar(
            self.current_year,
            self.current_month
        )

        for row_index, week in enumerate(
            month_calendar,
            start=1
        ):
            for column_index, day_number in enumerate(week):
                if day_number == 0:
                    continue

                selected = date(
                    self.current_year,
                    self.current_month,
                    day_number
                )

                button = tk.Button(
                    self.calendar_frame,
                    text=str(day_number),
                    width=3,
                    font=("Arial", 9)
                )

                if selected > self.today:
                    button.config(state=tk.DISABLED)
                else:
                    button.config(
                        command=lambda d=selected:
                        self.select_date(d)
                    )

                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=2,
                    pady=2
                )

        current_month_start = date(
            self.today.year,
            self.today.month,
            1
        )

        selected_month_start = date(
            self.current_year,
            self.current_month,
            1
        )

        if selected_month_start <= current_month_start:
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

        self.update_calendar()

    def next_month(self):
        if self.current_month == 12:
            new_year = self.current_year + 1
            new_month = 1
        else:
            new_year = self.current_year
            new_month = self.current_month + 1

        current_month_start = date(
            self.today.year,
            self.today.month,
            1
        )

        new_month_start = date(
            new_year,
            new_month,
            1
        )

        if new_month_start > current_month_start:
            return

        self.current_year = new_year
        self.current_month = new_month
        self.update_calendar()

    def select_date(self, selected_date):
        if selected_date > self.today:
            return

        self.callback(
            selected_date.strftime("%Y-%m-%d")
        )
        self.window.destroy()
