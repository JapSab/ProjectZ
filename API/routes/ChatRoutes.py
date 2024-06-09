from API import app, redis_cache, LIVECHAT_ORGANIZATION_ID, LIVECHAT_CLIENT_ID
from flask import  jsonify, request
import requests

from API.utils.livechat import call_livechat_api

@app.route('/get_customer_token', methods=['GET'])
def get_token():

    email = request.args.get('email')
    entity_id = request.args.get('entity_id')

    url = 'https://accounts.livechat.com/v2/customer/token'
    headers = {'Content-Type': 'application/json'}
    data = {
        "grant_type": "cookie",
        "client_id": LIVECHAT_CLIENT_ID,
        "organization_id": LIVECHAT_ORGANIZATION_ID,
        "response_type": "token"
    }

    if entity_id:
        data["entity_id"] = entity_id

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        if email:
            redis_cache.set(f"chat_token:{email}", response.json().get('access_token'), ex=14400)
            if entity_id:
                redis_cache.set(f"chat_entity:{email}", entity_id)
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to retrieve token", "status_code": response.status_code})


@app.route("/call_livechat", methods=['POST'])
def call_livechat():
    data = request.json if request.is_json else request.form.to_dict()
    action = data.get('action')
    if not action:
        return jsonify({"error": "Missing action parameter"}), 400

    if action == "get_chat" and not data.get("chat_id"):
        return jsonify({"error": "Missing chat_id for get_chat action"}), 400

    try:
        headers = {
            'Authorization': request.headers.get('Authorization'),
            'Content-Type': 'application/json'
        }
        response = call_livechat_api(action, params=data, headers=headers)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500