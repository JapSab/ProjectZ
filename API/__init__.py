from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DATABASE_NAME")
secret_key = os.getenv("SECRET_KEY")
jwt_secret_key = os.getenv("JWT_KEY")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['Clients']
jwt = JWTManager(app)
from API.routes import ClientAuth