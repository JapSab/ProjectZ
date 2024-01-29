from API import app
from flask import Flask, request, jsonify
from API.classes.Auth import ClientRegistration , ClientLogin, users_collection
import datetime


registration_handler = ClientRegistration(users_collection)

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        user_data = request.json
        result, status = registration_handler.register(user_data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        user_data = request.json
        email = user_data.get("email")
        password = user_data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        login_handler = ClientLogin(users_collection)
        result, status = login_handler.login(email, password)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

