import os

from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import redis

redis_cache = redis.Redis(host='redis-service', port=6379, decode_responses=True)

app = Flask(__name__)
CORS(app)

# mongo_uri = os.environ.get("localhost:27017")
mongo_uri = 'localhost:27017'

db_name = 'ProjectZ'
redis_url =  os.environ.get("REDIS_CACHE_URL")
secret_key = os.environ.get("SECRET_KEY")
jwt_secret_key = os.environ.get("JWT_KEY")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['Clients']
admin_collection = db['Admin']
blogs_collection = db['Blogs']
jwt = JWTManager(app)

# ChatAPI Routes
API_VERSION = "v3.5"
ORGANIZATION_ID = "806b6f60-0f08-4f4d-a3cf-0d84d73d88c5"



def teardown_event(exception=None):
    if redis_cache.redis_cache is not None:
        redis_cache.redis_cache.close()


@app.route("/healthz")
async def root():

    return jsonify({"message": "PONG"})


from API.routes import ClientAuth
from API.routes import AdminRoutes
from API.routes import BlogRoutes
from API.routes import ChatRoutes