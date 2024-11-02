# usage

`.env.template`をコピーして、`.env`を作成する。
JWT_SECRET_KEYに任意のキーを設定する。

以下コマンドでコンテナを立ち上げる。
```bash
docker-compose up --build
```


```bash
# ユーザーを作成
curl -X POST http://localhost:5001/user/signup -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}'

# tokenを取得
export TOKEN=$(curl -X POST http://localhost:5001/user/signin -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' | jq -r .access_token)

# dummyAPIにリクエストを投げる
curl -X POST http://localhost:5002/dummyservice -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"x1": 1, "x2":2}'

# optimizeAPIにリクエストを投げ、dummyAPIの最小値を求める
curl -X POST http://localhost:5003/optimize -H "Authorization: Bearer $TOKEN"
```