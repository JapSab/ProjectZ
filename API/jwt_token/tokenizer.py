from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import jsonify

def generate_jwt_token(identity, role):
    additional_claims = {"role": role}
    return create_access_token(identity=identity, additional_claims=additional_claims)


def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Admin rights required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper