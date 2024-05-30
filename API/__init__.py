import os

from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import redis

redis_cache = redis.Redis(host='redis-service', port=6379, decode_responses=True)

app = Flask(__name__)
CORS(app)

mongo_uri = os.environ.get("MONGO_URI")
#mongo_uri = 'localhost:27017'

db_name = 'ProjectZ'
secret_key = os.environ.get("SECRET_KEY")
jwt_secret_key = os.environ.get("JWT_KEY")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['Clients']
admin_collection = db['Admin']
blogs_collection = db['Blogs']
jwt = JWTManager(app)

# ChatAPI Envs
LIVECHAT_BASE_URL = "https://api.livechatinc.com"
LIVECHAT_API_VERSION = "v3.5"
LIVECHAT_ORGANIZATION_ID = "806b6f60-0f08-4f4d-a3cf-0d84d73d88c5"

# TBCPay Envs
TBCPAY_BASE_URL = "https://api.tbcbank.ge"
TBCPAY_API_VERSION = "v1"
TBCPAY_API_KEY = "SXxJe9d2ZGVc7VpZROdMRRGh7KFrx63G"
TBCPAY_CLIENT_ID = "7001798"
TBCPAY_CLIENT_SECRET = "tq2h0YMXvNr9eA1u"


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
from API.routes import TBCPayRoutes