import os
import optuna
import requests
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')
jwt = JWTManager(app)

@app.route('/optimize', methods=['POST'])
@jwt_required()
def optimize():
    token = request.headers.get("Authorization")  # JWTトークンをヘッダーから取得

    # Optunaの目的関数
    def objective(trial):
        x1 = trial.suggest_uniform('x1', -10, 10)
        x2 = trial.suggest_uniform('x2', -10, 10)

        # dummyAPIにパラメータを送信
        response = requests.post(
            'http://localhost:5001/dummyservice',  # dummyAPIのURL
            json={'x1': x1, 'x2': x2},
            headers={'Authorization': token}
        )

        if response.status_code == 200:
            y = response.json().get('y')
            return y
        else:
            return float('inf')  # エラーが発生した場合、高い値を返す

    # Optunaのスタディ作成と最適化実行
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=50)

    # 最適なパラメータと目的値を返す
    return jsonify(
        best_params=study.best_params,
        best_value=study.best_value
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)  # ポートは任意
