import os
from flask import Flask
from flask_cors import CORS
from models import db
from user_routes import user_blueprint
from flask_jwt_extended import JWTManager
import datetime

# environ
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_EXPIRE_SECONDS = int(os.environ.get("JWT_EXPIRE_SECONDS"))

# flask-app
app = Flask(__name__)
CORS(app)

# dbの設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# dbの初期化
db.init_app(app)
with app.app_context():
    db.create_all()

# blueprintの登録
app.register_blueprint(user_blueprint, url_prefix="/user")

# JWTのキーを設定。環境変数に設定されていない場合はエラーを返す
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=JWT_EXPIRE_SECONDS)
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
