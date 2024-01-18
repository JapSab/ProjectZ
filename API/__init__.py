from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DATABASE_NAME")
secret_key = os.getenv("SECRET_KEY")

client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['Clients']

from API.routes import ClientAuth