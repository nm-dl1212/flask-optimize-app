import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_shared_secret_key')
jwt = JWTManager(app)


# メモリ内にダミーデータを格納する簡易データベース
users = {}

# サインアップエンドポイント
@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    if username in users:
        return jsonify({"msg": "Username already exists"}), 400
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    return jsonify({"msg": "User created successfully"}), 201

# サインインエンドポイント
@app.route('/signin', methods=['POST'])
def signin():
    username = request.json.get("username")
    password = request.json.get("password")
    user_password = users.get(username)

    if not user_password or not check_password_hash(user_password, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# ユーザー削除エンドポイント
@app.route('/delete_user', methods=['DELETE'])
@jwt_required()
def delete_user():
    username = get_jwt_identity()
    if username in users:
        del users[username]
        return jsonify({"msg": "User deleted successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
