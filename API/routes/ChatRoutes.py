from API import app
from flask import  jsonify, request
import requests

from API.utils.livechat import call_livechat_api

@app.route('/get_customer_token', methods=['GET'])
def get_token():
    url = 'https://accounts.livechat.com/v2/customer/token'
    headers = {'Content-Type': 'application/json'}
    data = {
        "grant_type": "cookie",
        "client_id": "041ee1815aab416ec9f39245e548c650",
        "organization_id": "806b6f60-0f08-4f4d-a3cf-0d84d73d88c5",
        "response_type": "token"
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to retrieve token", "status_code": response.status_code})


@app.route("/call_livechat", methods=['POST'])
def call_livechat():
    data = request.json if request.is_json else request.form.to_dict()
    action = data.get('action')
    if not action:
        return jsonify({"error": "Missing action parameter"}), 400

    if action == "get_chat" and (not data.get("chat_id") or not data.get("thread_id")):
        return jsonify({"error": "Missing chat_id or thread_id for get_chat action"}), 400

    try:
        headers = {
            'Authorization': request.headers.get('Authorization'),
            'Content-Type': 'application/json'
        }
        response = call_livechat_api(action, params=data, headers=headers)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500