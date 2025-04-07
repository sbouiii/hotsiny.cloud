from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.config import Config

# MongoDB connection
client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
db = client['hosting_platform']
messages_collection = db['messages']

def init_mongo(app):
    # Test MongoDB connection
    try:
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")