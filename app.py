from database import initialize_database
from gui.main_window import ExpenseTrackerApp


if __name__ == "__main__":
    initialize_database()
    app = ExpenseTrackerApp()
    app.run()
