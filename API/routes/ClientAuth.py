from API import app, redis_cache
from flask import request, jsonify
from API.classes.Auth import ClientRegistration , ClientLogin, users_collection
import datetime
import json


registration_handler = ClientRegistration(users_collection)

@app.route('/api/client/register', methods=['POST'])
def register_user():
    try:
        user_data = request.json
        result, status = registration_handler.register(user_data)
        return jsonify(result), status
    except Exception as e:
        app.logger.error(f"Failed to register user: {str(e)}")  # Log the error in more detail
        return jsonify({"error": str(e)}), 500


@app.route('/api/client/login', methods=['POST'])
def login_user():
    try:
        user_data = request.json
        email = user_data.get("email")
        password = user_data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        login_handler = ClientLogin(users_collection)
        result, status = login_handler.login(email, password)
        # redis_cache.set(email, json.dumps({'token:': result.get("token")}), ex=datetime.timedelta(days=1))
        print(result)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/client/logout', methods=['POST'])
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