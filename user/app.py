import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

dummy_users = {
    "user1": "password1",
    "user2": "password2"
}

@app.route('/user', methods=['POST'])
def user_login():
    username = request.json.get("username")
    password = request.json.get("password")
    if dummy_users.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
