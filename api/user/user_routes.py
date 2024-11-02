from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

user_blueprint = Blueprint('user', __name__)


# サインアップエンドポイント
@user_blueprint.route('/signup', methods=['POST'])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


# サインインエンドポイント
@user_blueprint.route('/signin', methods=['POST'])
def signin():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# ユーザー削除エンドポイント
@user_blueprint.route('/delete_user', methods=['DELETE'])
@jwt_required()
def delete_user():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404
