import os
import time
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# environ
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# flask-app
app = Flask(__name__)

# JWTのキーを設定。環境変数に設定されていない場合はエラーを返す
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)


@app.route("/dummy", methods=["POST"])
@jwt_required()
def dummy():
    current_user = get_jwt_identity()

    x1 = request.json.get("x1")
    x2 = request.json.get("x2")
    y = x1**2 + x2 * 0.5
    time.sleep(0.2)  # ダミーの待ち時間

    return (
        jsonify(msg=f"Hello, {current_user}. This is a dummy service response.", y=y),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
