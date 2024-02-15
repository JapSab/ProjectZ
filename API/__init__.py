import os

from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .connections import RedisCache, redis_cache

app = Flask(__name__)
CORS(app)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DATABASE_NAME")
redis_url = os.environ.get("REDIS_CACHE_URL")
secret_key = os.environ.get("SECRET_KEY")
jwt_secret_key = os.environ.get("JWT_KEY")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['Clients']
admin_collection = db['Admin']
blogs_collection = db['Blogs']
jwt = JWTManager(app)


def teardown_event(exception=None):
    if redis_cache.redis_cache is not None:
        redis_cache.redis_cache.close()


@app.route("/healthz")
async def root():
    if redis_cache.redis_cache is None:
        raise RuntimeError("Redis cache is not initialized")

    await redis_cache.set("healthz", "PONG")
    return jsonify({"message": "PONG"})


from API.routes import ClientAuth
from API.routes import AdminRoutes
from API.routes import BlogRoutes