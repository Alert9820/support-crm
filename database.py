from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["support_crm"]
tickets_collection = db["tickets"]
notes_collection = db["notes"]
