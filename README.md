# usage
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