from datetime import datetime, timedelta
from typing import Union
import os

import uvicorn

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel


# JWT 表示 「JSON Web Tokens」。
# 它是一个将 JSON 对象编码为密集且没有空格的长字符串的标准。字符串看起来像这样：
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
# 它没有被加密，因此任何人都可以从字符串内容中还原数据。
# 但它经过了签名。因此，当你收到一个由你发出的令牌时，可以校验令牌是否真的由你发出。
# 通过这种方式，你可以创建一个有效期为 1 周的令牌。
# 然后当用户第二天使用令牌重新访问时，你知道该用户仍然处于登入状态。
# 一周后令牌将会过期，用户将不会通过认证，必须再次登录才能获得一个新令牌。
# 而且如果用户（或第三方）试图修改令牌以篡改过期时间，你将因为签名不匹配而能够发觉。
# 如果你想上手体验 JWT 令牌并了解其工作方式，可访问 https://jwt.io

# 我们需要安装 python-jose 以在 Python 中生成和校验 JWT 令牌：
# pip install python-jose[cryptography]
# Python-jose 需要一个额外的加密后端。
# 这里我们使用的是推荐的后端：pyca/cryptography。
# 本教程曾经使用过 PyJWT。
# 但是后来更新为使用 Python-jose，
# 因为它提供了 PyJWT 的所有功能，以及之后与其他工具进行集成时你可能需要的一些其他功能。

# 安装 passlib
# PassLib 是一个用于处理哈希密码的很棒的 Python 包。
# 它支持许多安全哈希算法以及配合算法使用的实用程序。
# 推荐的算法是 「Bcrypt」。
# 因此，安装附带 Bcrypt 的 PassLib：
# pip install passlib[bcrypt]
# 使用 passlib，你甚至可以将其配置为能够读取 Django，Flask 的安全扩展或许多其他工具创建的密码。



# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SECRET_KEY 等价于这样生成 不用ssl
# from secrets import token_bytes
# from base64 import b64encode
# print(b64encode(token_bytes(32)).decode())

# pw
# secret
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjY2NTc4ODM3fQ.i-bXcDZ4RHzP1Q7RlV1ULX228OBJN9-s4w1xNaRQjU8'
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# 忘了 再记录一次
# response_model是「装饰器」方法（get，post 等）的一个参数。
# 不像之前的所有参数和请求体，它不属于路径操作函数。
# FastAPI 将使用此 response_model 来：
# 将输出数据转换为其声明的类型。
# 校验数据。
# 在 OpenAPI 的路径操作中为响应添加一个 JSON Schema。
# 并在自动生成文档系统中使用。
# 就是收到请求后，要返回的东西格式？大概。
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/users/me/pw")
async def read_users_me(current_user_hash: str = Depends(get_password_hash)):
    return current_user_hash
# $2b$12$Pp9kJz2byAMVpXejHgK4EOOGC79Ng4jpYLQ8pHF6cizcj9zf5aYoC




# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)