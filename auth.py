from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

SECRET_KEY = "your-secret-key"

def create_access_token(payload: dict):
    # 这个exp是固定的字符串，不能改
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=3)
    return jwt.encode(payload, SECRET_KEY)

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception:
        return None

PUBLIC_PATHS = ["/", "/docs", "/redoc", "/users/createUser", "/users/login"]
async def auth_middleware(request: Request, call_next):
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(content={"msg": "缺少认证信息", 'status_code': 401})
    
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else auth_header
    payload = verify_token(token)
    if not payload:
        return JSONResponse(content={"msg": "无效的token或token已过期", 'status_code': 401})
    
    request.state.username = payload.get("username")

    response = await call_next(request)
    return response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)