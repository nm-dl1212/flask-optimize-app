# usage
```bash
docker-compose up --build
```


```bash
# ユーザーを作成
curl -X POST http://localhost:5001/user/signup -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}'

# tokenを取得＆リクエスト
export TOKEN=$(curl -X POST http://localhost:5001/user/signin -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' | jq -r .access_token)
curl -X POST http://localhost:5002/dummyservice -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"x1": 1, "x2":2}'
```