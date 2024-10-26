# usage
```bash
docker-compose up --build
```

```bash
export TOKEN=$(curl -X POST http://localhost:5001/user -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' | jq -r .access_token)
curl -X GET http://localhost:5002/dummyservice -H "Authorization: Bearer $TOKEN"
```