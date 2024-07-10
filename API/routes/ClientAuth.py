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
        email = user_data.get("email")
        result, status = registration_handler.register(user_data)
        email_token = registration_handler.generate_verification_token(email)
        verification_link = f"http://frontend.com/verify-email?token={email_token}"
        # send_verification_email(email, verification_link)

        return jsonify(result), status

    except Exception as e:
        app.logger.error(f"Failed to register user: {str(e)}")  # Log the error in more detail

        return jsonify({"error": str(e)}), 500


@app.route('/api/client/verify', methods=['POST'])
def verify_email():
    email = registration_handler.verify_token(token)
    token = user_data.get("token")

    if not email:
        return jsonify({'message': 'The verification link is invalid or has expired.'}), 400
    registration_handler.verify_email(email)
   
    return jsonify({'message': 'Your email has been verified!'}), 200

 
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

        redis_cache.delete(f"login_token:{email}")

        return jsonify({"message": "User logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500