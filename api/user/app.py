import os
from flask import Flask
from flask_cors import CORS
from models import db
from user_routes import user_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLiteデータベースを指定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# blueprintの登録
app.register_blueprint(user_blueprint, url_prefix='/user')

# 環境変数からJWTのキーを取得。設定されていない場合はエラーを返す
jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
if not jwt_secret_key:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

# データベースの初期化
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
