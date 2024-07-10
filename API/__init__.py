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

LIVECHAT_BASE_URL = os.environ.get("LIVECHAT_BASE_URL")
LIVECHAT_API_VERSION = os.environ.get("LIVECHAT_API_VERSION")
LIVECHAT_ORGANIZATION_ID = os.environ.get("LIVECHAT_ORGANIZATION_ID")
LIVECHAT_CLIENT_ID = os.environ.get("LIVECHAT_CLIENT_ID")

TBCPAY_BASE_URL = os.environ.get("TBCPAY_BASE_URL")
TBCPAY_API_VERSION = os.environ.get("TBCPAY_API_VERSION")
TBCPAY_API_KEY = os.environ.get("TBCPAY_API_KEY")
TBCPAY_CLIENT_ID = os.environ.get("TBCPAY_CLIENT_ID")
TBCPAY_CLIENT_SECRET = os.environ.get("TBCPAY_CLIENT_SECRET")

MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', 'sandbox123.mailgun.org')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', 'YOUR_MAILGUN_API_KEY')
MAILGUN_SENDER_EMAIL = os.getenv('MAILGUN_SENDER_EMAIL', 'no-reply@sandbox123.mailgun.org')

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