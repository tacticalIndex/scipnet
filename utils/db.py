import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
ENVIRONMENT = os.getenv("ENVIRONMENT")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in the environment variables.")

client = MongoClient(MONGO_URI)
db = client["scipnet"]