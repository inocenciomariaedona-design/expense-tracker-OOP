class CategoryManager:
    def __init__(self, max_categories):
        self.categories = [
            "Food",
            "Transportation",
            "Shopping",
            "Bills"
        ]
        self.max_categories = max_categories

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
            return old_category, new_category

        return None

    def delete_category(self, index):
        if 0 <= index < len(self.categories):
            return self.categories.pop(index)

        return None

    def can_add_category(self):
        return len(self.categories) < self.max_categories

    def get_remaining_slots(self):
        return self.max_categories - len(self.categories)
