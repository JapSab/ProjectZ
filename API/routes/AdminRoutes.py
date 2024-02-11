from API import app
from flask import request, jsonify
from API.classes.Auth import AdminLogin, admin_collection
from API.jwt_token.tokenizer import admin_required

# attorney_handler = AdminLogin(admin_collection)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        admin_data = request.json
        username = admin_data.get("username")
        password = admin_data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        attorney_handler = AdminLogin(admin_collection)
        result, status = attorney_handler.login(username, password)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# later if necessary
@app.route('/api/admin/panel', methods=['GET'])
@admin_required
def get_admin_panel():
    pass



