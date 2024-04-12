from API import app
from flask import request, jsonify
from API.classes.Auth import ClientRegistration , ClientLogin, users_collection
from API import redis_cache
import datetime
import json


registration_handler = ClientRegistration(users_collection)

@app.route.route('/api/client/register', methods=['POST'])
def register_user():
    try:
        user_data = request.json
        result, status = registration_handler.register(user_data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route.route('/api/client/login', methods=['POST'])
def login_user():
    try:
        user_data = request.json
        email = user_data.get("email")
        password = user_data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        login_handler = ClientLogin(users_collection)
        result, status = login_handler.login(email, password)
        redis_cache.set(email, json.dumps({'token:': result.get("token")}), ex=datetime.timedelta(days=1))
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route.route('/api/client/logout', methods=['POST'])
def logout_user():
    try:
        user_data = request.json
        email = user_data.get("email")

        if not email:
            return jsonify({"error": "Missing email"}), 400

        redis_cache.delete(email)

        return jsonify({"message": "User logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500