import os

from pymongo import MongoClient
from pymongo import ReturnDocument


DEFAULT_CATEGORIES = (
    "Food",
    "Transportation",
    "Shopping",
    "Bills",
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("EXPENSE_DB_NAME", "expense_tracker")

client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]
expenses_collection = database["expenses"]
categories_collection = database["categories"]
settings_collection = database["settings"]


def initialize_database():
    marker = settings_collection.find_one_and_update(
        {"_id": "categories_seeded"},
        {"$setOnInsert": {"initialized": True}},
        upsert=True,
        return_document=ReturnDocument.BEFORE,
    )

    if marker is None:
        categories_collection.insert_many(
            {"name": category}
            for category in DEFAULT_CATEGORIES
        )

        settings_collection.update_one(
            {"_id": "categories_seeded"},
            {"$set": {"initialized": True}},
            upsert=True,
        )

    return database


def get_categories():
    initialize_database()
    return [
        item["name"]
        for item in categories_collection.find().sort("_id", 1)
    ]


def save_categories(categories):
    initialize_database()
    categories_collection.delete_many({})

    if categories:
        categories_collection.insert_many(
            {"name": category}
            for category in categories
        )

    settings_collection.update_one(
        {"_id": "categories_seeded"},
        {"$set": {"initialized": True}},
        upsert=True,
    )


def get_expenses():
    initialize_database()
    return list(expenses_collection.find({}).sort("_id", 1))


def save_expenses(expenses):
    initialize_database()
    expenses_collection.delete_many({})

    if expenses:
        expenses_collection.insert_many(expenses)

    settings_collection.update_one(
        {"_id": "categories_seeded"},
        {"$set": {"initialized": True}},
        upsert=True,
    )