from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import os

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DATABASE_NAME")
secret_key = os.environ.get("SECRET_KEY")
jwt_secret_key = os.environ.get("JWT_KEY")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['Clients']
admin_collection = db['Admin']
blogs_collection = db['Blogs']
jwt = JWTManager(app)

from API.routes import ClientAuth
from API.routes import AdminRoutes
from API.routes import BlogRoutes