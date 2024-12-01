import os
import optuna
import requests
from flask import Flask, jsonify, request, Response, stream_with_context
from flask_jwt_extended import JWTManager, jwt_required

# environ
DUMMY_URL = os.environ["DUMMY_URL"]
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# flask-app
app = Flask(__name__)

# JWTのキーを設定。環境変数に設定されていない場合はエラーを返す
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)


# api endpoint
@app.route("/optimize", methods=["POST"])
@jwt_required()
def optimize():
    token = request.headers.get("Authorization")  # JWTトークンをヘッダーから取得

    # Optunaの目的関数
    def objective(trial):
        x1 = trial.suggest_uniform("x1", -10, 10)
        x2 = trial.suggest_uniform("x2", -10, 10)

        # dummyAPIにパラメータを送信
        response = requests.post(
            DUMMY_URL,
            json={"x1": x1, "x2": x2},
            headers={"Authorization": token},
        )

        if response.status_code == 200:
            y = response.json().get("y")
            return y
        else:
            return float("inf")  # エラーが発生した場合、高い値を返す

    # ストリーミング応答を生成
    @stream_with_context
    def generate():
        study = optuna.create_study(direction="minimize")
        for i in range(50):
            # optunaの最適化を実行
            study.optimize(objective, n_trials=1)  # 1回ずつ実行

            # 最新のデータ
            latest_trial = study.trials[-1]

            # これまでの最良値
            best_trial = study.best_trial

            response_json = jsonify(
                {
                    "best": {
                        "number": best_trial.number,
                        "params": best_trial.params,
                        "value": best_trial.value,
                    },
                    "latest": {
                        "number": latest_trial.number,
                        "params": latest_trial.params,
                        "value": latest_trial.value,
                    },
                }
            )
            yield f"{response_json.get_data(as_text=True)}"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)  # ポートは任意
