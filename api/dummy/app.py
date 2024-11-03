import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 環境変数からJWTのキーを取得。設定されていない場合はエラーを返す
jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
if not jwt_secret_key:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

@app.route('/dummy', methods=['POST'])
@jwt_required()
def dummy():
    current_user = get_jwt_identity()
    
    print("dummy_function")
    x1 = request.json.get("x1")
    x2 = request.json.get("x2")
    y = x1**2 + x2*0.5

    return jsonify(msg=f"Hello, {current_user}. This is a dummy service response.", y=y), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)