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
    return [i.to_dict() for i in users]

@router.post("/changeUser")
async def change_user(request: Request):
    try:
        body = await request.json()
        username = body.get("username")
        oldpassword = body.get("oldpassword")
        newpassword = body.get("newpassword")
        version = body.get("version")

        if not username or not oldpassword or not newpassword:
            return {"status_code": 400, "msg": "用户名或密码不能为空"}

        user = await User.filter(username=username).first()
        if not verify_password(oldpassword, user.password):
            return {"status_code": 400, "msg": "密码错误"}
        if user.version != version:
            return {"status_code": 400, 'msg': '版本错误'}

        # 原子性
        count = await User.filter(username=username, version=version).update(password=hash_password(newpassword), version=version+1)
        if count == 0:
            return {"status_code": 400, 'msg': '修改密码冲突，刷新之后再试'}
        
        return {"status_code": 200, 'msg': '用户修改密码成功'}
    except Exception as e:
        return {"status_code": 400, "msg": str(e)}
