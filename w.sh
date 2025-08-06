curl -X POST "http://localhost:8000/users/createUser" -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'
curl -X POST "http://localhost:8000/users/login" -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'

curl -X GET "http://localhost:8000/users/getAllUsers" -H "Authorization: Bearer xxxxxxx"
curl -X POST "http://localhost:8000/users/changeUser" -H "Authorization: Bearer xxxxxxx" -d '{"username": "test", "oldpassword": "test", "newpassword": "123", "version"=0}'