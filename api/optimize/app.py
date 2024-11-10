import os
import optuna
import requests
from flask import Flask, jsonify, request, Response, stream_with_context
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)

# 環境変数からJWTのキーを取得。設定されていない場合はエラーを返す
jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
if not jwt_secret_key:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
app.config['JWT_SECRET_KEY'] = jwt_secret_key
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
            'http://dummy_service:5002/dummy',  # dummyAPIのURL
            json={'x1': x1, 'x2': x2},
            headers={'Authorization': token}
        )

        if response.status_code == 200:
            y = response.json().get('y')
            return y
        else:
            return float('inf')  # エラーが発生した場合、高い値を返す

   # ストリーミング応答を生成
    @stream_with_context
    def generate():
        study = optuna.create_study(direction='minimize')
        for trial in range(50):
            study.optimize(objective, n_trials=1)  # 1回ずつ実行
            
            # 最新のデータ
            latest_trial = study.trials[-1]
            latest_x = latest_trial.params
            latest_y= latest_trial.value

            # これまでの最良値
            best_x = study.best_params
            best_y = study.best_value

            yield f"{jsonify({'best_x': best_x, 'best_y': best_y, 'latest_x': latest_x, 'latest_y': latest_y}).get_data(as_text=True)}"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)  # ポートは任意
