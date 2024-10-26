import os
from flask import Flask
from models import db
from user_routes import user_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_shared_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLiteデータベースを指定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# blueprintの登録
app.register_blueprint(user_blueprint, url_prefix='/user')

# jwtmanagerの初期化
jwt = JWTManager(app)

# データベースの初期化
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
