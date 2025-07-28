from fastapi import APIRouter, Request
from models import User
from auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/login")
async def login(request: Request):
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return {"status_code": 400, "msg": "用户名或密码不能为空"}

        user = await User.get_or_none(username=username)
        if not user:
            return {"status_code": 400, "msg": "用户名错误"}
        if not verify_password(password, user.password):
            return {"status_code": 400, "msg": "密码错误"}

        token = create_access_token({"username": username})
        return {"token": token, "username": username}
    except Exception as e:
        return {"status_code": 400, "msg": str(e)}

@router.post("/createUser")
async def create_user(request: Request):
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return {"status_code": 400, "msg": "用户名或密码不能为空"}

        existing_user = await User.get_or_none(username=username)
        if existing_user:
            return {"status_code": 400, "msg": "用户名已存在"}

        pw = hash_password(password)
        user = await User.create(username=username, password=pw)
        return {"status_code": 200, 'msg': '用户创建成功', 'username': username, 'id': user.id}
    except Exception as e:
        return {"status_code": 400, "msg": str(e)}

@router.get("/getAllUsers")
async def get_users():
    users = await User.all()
    return await User.list_to_dict(users)

