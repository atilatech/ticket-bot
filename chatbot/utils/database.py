from collections import defaultdict

from pymongo import MongoClient
from utils.credentials import MONGODB_URL, MONGODB_USERNAME, MONGODB_PASSWORD

USERS_TABLE = 'ticketbot_users'

# Provide the mongodb atlas url to connect python to mongodb using pymongo

connection_string = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_URL}"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(connection_string)
database = client['atila']


def save_data(data, table_name=USERS_TABLE):
    database[table_name].insert_one(data)


def update_user(user_id, new_data):
    database[USERS_TABLE].update_one({'user_id': user_id}, {'$set': new_data})
