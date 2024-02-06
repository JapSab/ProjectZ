from API import  users_collection, admin_collection,jwt_secret_key
import bcrypt, datetime
import jwt
from API.jwt_token.tokenizer import generate_jwt_token 

class ClientRegistration:
    def __init__(self, users_collection):
        self.users_collection = users_collection

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def register(self, user_data):
        name = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        phone = user_data.get("phone")

        # validation
        if not name or not email or not phone or not password:
            return {"error": "Missing name, email, or phone"}, 400

        # Check if user already exists
        if self.users_collection.find_one({"email": email}):
            return {"error": "User with this email already exists"}, 409

        # hashing the password
        hashed_password = self.hash_password(password)
        user_data['password'] = hashed_password

        user_data = {
            "username": name,
            "email": email,
            "password": hashed_password,
            "phone": phone,
            "role": "user"  
        }

        # Inserting user data into MongoDB
        self.users_collection.insert_one(user_data)
        return {"message": "User registered successfully"}, 201
    

class ClientLogin:
    def __init__(self, users_collection):
        self.users_collection = users_collection
        self.secret_key = jwt_secret_key

    def verify_password(self, stored_password, provided_password):
        """Verify a stored hashed password against one provided by user"""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def login(self, email, password):
        # Find user by email
        user = self.users_collection.find_one({"email": email})
        
        if not user:
            return {"error": "No user found with that email"}, 404

        # Verify the password
        if not self.verify_password(user['password'], password):
            return {"error": "Invalid password"}, 401
        # if self.verify_password(user['password'], password):
        #     payload = {
        #         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        #         'iat': datetime.datetime.utcnow(),
        #         'sub': user['email'],
        #         'name': user.get('name', '')
        #     }
        #     token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        #     return {"message": "Login successful", "token": token}, 200
        identity = {'email': user['email'], 'name': user.get('username', '')}
        access_token = generate_jwt_token(identity, role=user.get('role'))
        return {"message": "Login successful", "token": access_token}, 200
    

class AdminLogin:
    def __init__(self, admin_collection):
        self.admin_collection = admin_collection
        self.secret_key = jwt_secret_key

    def verify_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def login(self, name, password):
        # Find user by email
        admin = self.admin_collection.find_one({"username": name})
        if not admin:
            return {"error": "Wrong username."}, 401

        
        # Verify the password
        if not self.verify_password(admin['password'], password):
            return {"error": "Invalid password"}, 401
        
        identity = {'name': admin.get('username', '')}
        access_token = generate_jwt_token(identity, role=admin.get('role'))
        return {"message": "Login successful", "token": access_token}, 200
    