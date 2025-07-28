curl -X GET "http://localhost:8000/users/getAllUsers"
curl -X POST "http://localhost:8000/users/createUser" -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'
curl -X POST "http://localhost:8000/users/login" -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'

curl -X GET "http://localhost:8000/users/getAllUsers" -H "Authorization: Bearer xxxxxxx"