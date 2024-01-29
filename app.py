from API import app
from flask_jwt_extended import jwt_required, get_jwt_identity



@app.route('/dashboard')
@jwt_required()
def hello():
    identity = get_jwt_identity()
    user_name = identity.get('name', 'guest')
    return 'Hello, ' + user_name


if __name__ == '__main__':
    app.run(debug=True)
