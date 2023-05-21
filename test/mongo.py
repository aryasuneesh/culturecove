from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv.main import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://aryasuneesh3:{DB_PASSWORD}@ccluster.a0eszym.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)