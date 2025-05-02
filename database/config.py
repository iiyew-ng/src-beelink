from pymongo import MongoClient
from dotenv import load_dotenv
import os


def get_db():

    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client['shortener']
    users = db['users']
    urls = db['urls']

    return users, urls