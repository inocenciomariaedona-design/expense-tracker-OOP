class CategoryManager:
    def __init__(self, max_categories):
        self.categories = []
        self.max_categories = max_categories
        self._load_from_database()

    def _load_from_database(self):
        try:
            from database import initialize_database, get_categories

            initialize_database()
            database_categories = get_categories()

            if database_categories:
                self.categories = database_categories
            else:
                self.categories = [
                    "Food",
                    "Transportation",
                    "Shopping",
                    "Bills",
                ]
        except Exception:
            self.categories = [
                "Food",
                "Transportation",
                "Shopping",
                "Bills",
            ]

    def _persist_to_database(self):
        try:
            from database import save_categories

            save_categories(self.categories)
        except Exception:
            pass

    def get_categories(self):
        return self.categories

    def add_category(self, category):
        category = category.strip()

        if (
            category
            and category not in self.categories
            and len(self.categories) < self.max_categories
        ):
            self.categories.append(category)
            self._persist_to_database()
            return True

        return False

    def edit_category(self, index, new_category):
        new_category = new_category.strip()

        if (
            0 <= index < len(self.categories)
            and new_category
            and new_category not in self.categories
        ):
            old_category = self.categories[index]
            self.categories[index] = new_category
            self._persist_to_database()
            return old_category, new_category

        return None

    def delete_category(self, index):
        if 0 <= index < len(self.categories):
            deleted = self.categories.pop(index)
            self._persist_to_database()
            return deleted

        return None

    def can_add_category(self):
        return len(self.categories) < self.max_categories

    def get_remaining_slots(self):
        return self.max_categories - len(self.categories)
