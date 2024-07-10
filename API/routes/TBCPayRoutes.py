from API import app, redis_cache
from flask import  jsonify, request
import requests

from API.utils.tbcpay import call_tbcpay_api

@app.route('/call_tbcpay', methods=['POST'])
def call_tbcpay():
    data = request.json if request.is_json else request.form.to_dict()
    action = data.get('action')
    if not action:
        return jsonify({"error": "Missing action parameter"}), 400
    try:
        response = call_tbcpay_api(action, params=data)
        print(response)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500