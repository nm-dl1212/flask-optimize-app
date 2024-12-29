# 概要
1. user サービス
    - サインアップ
    - URL: /signup
        - メソッド: POST
        - 説明: ユーザーを新規登録します。
        - リクエスト: { "username": "string", "password": "string" }
        - レスポンス: {"message": "User created successfully."}
        - ログイン
    - URL: /login
        - メソッド: POST
        - 説明: ログインしてJWTトークンを取得します。
        - リクエスト: { "username": "string", "password": "string" }
        - レスポンス: { "access_token": "string" }
2. dummy サービス
    - ダミー計算
    - URL: /dummy
        - メソッド: POST
        - 説明: 与えられたパラメータをもとに数値計算します。
        - 認証: 必要（JWTトークン）
        - リクエスト: { "x1": "number", "x2": "number" }
        - レスポンス: { "y": "number" }
3. optimize サービス
    - 最適化
    - URL: /optimize
        - メソッド: POST
        - 説明: dummy APIを使用し、パラメータの最適化を行います。
        - 認証: 必要（JWTトークン）
        - リクエスト: { "initial_x1": "number", "initial_x2": "number", "n_trials": "integer" }
        - レスポンス:
        - results: それぞれの試行結果のリスト
        - min_result: 全体での最小値

# 初期設定
`.env.template`をコピーして、`.env`を作成する。
JWT_SECRET_KEYに任意のキーを設定する。

以下コマンドでコンテナを立ち上げる。
```bash
docker-compose up --build
```

# 使用方法
```bash
# ユーザーを作成
curl -X POST http://localhost:5001/user/signup -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}'

# tokenを取得
export TOKEN=$(curl -X POST http://localhost:5001/user/signin -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' | jq -r .access_token)

# dummyAPIにリクエストを投げる
curl -X POST http://localhost:5002/dummy -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"x1": 1, "x2":2}'

# optimizeAPIにリクエストを投げ、dummyAPIの最小値を求める
curl -X POST http://localhost:5003/optimize -H "Authorization: Bearer $TOKEN"
```



# kubernetes

```bash
# minikubeを起動
minikube start
eval $(minikube docker-env)


# コンテナをビルド
docker build -t streamlit-service streamlit/
docker build -t user-service api/user/
docker build -t dummy-service api/dummy/
docker build -t optimize-service api/optimize/


# 名前空間
kubectl create namespace opt-app

# シークレットを登録
kubectl apply -f k8s/jwt-secret.yaml -n opt-app
kubectl describe secret jwt-secret -n opt-app

# デプロイ
kubectl apply -f k8s/user-service-deployment.yaml,k8s/dummy-service-deployment.yaml,k8s/optimize-service-deployment.yaml,k8s/streamlit-service-deployment.yaml -n opt-app


# サービスにポートフォワード
kubectl port-forward svc/streamlit 30001:8501 -n opt-app

# 削除
kubectl delete ns opt-app
```