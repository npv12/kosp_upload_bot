import pymongo
from bot import MONGO_URL, DB_NAME


def init():
    client = pymongo.MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db
