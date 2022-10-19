from typing import Union, List, Dict

import uvicorn

from fastapi import FastAPI, status, Form, File, UploadFile
from pydantic import BaseModel, EmailStr
from fastapi.responses import HTMLResponse

app = FastAPI()

# 有pw
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

# 无pw 响应体
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

# db hash
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


# 大体思路是
# /user/ 收到userin
# 然后 fake_save...()
# pw加前缀，解包userin
# 转存密码
# 返回userindb
# 相应userout
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

# user_in 是一个 UserIn 类的 Pydantic 模型.
# Pydantic 模型具有 .dict（） 方法，该方法返回一个拥有模型数据的 dict。
# ** 解包
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

# user_dict = user_in.dict()
# UserInDB(**user_dict)
# UserInDB(
#     username="john",
#     password="secret",
#     email="john.doe@example.com",
#     full_name=None,
# )
#
# UserInDB(
#     username = user_dict["username"],
#     password = user_dict["password"],
#     email = user_dict["email"],
#     full_name = user_dict["full_name"],
# )
# == UserInDB(**user_in.dict())
#
# hashed_password=hashed_password
# UserInDB(
#     username = user_dict["username"],
#     password = user_dict["password"],
#     email = user_dict["email"],
#     full_name = user_dict["full_name"],
#     hashed_password = hashed_password,
# )

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# 整合class写法（继承
class UserBase_class(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn_class(UserBase_class):
    password: str

class UserOut_class(UserBase_class):
    pass

class UserInDB_class(UserBase_class):
    hashed_password: str


def fake_password_hasher_class(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn_class):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB_class(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user_class/", response_model=UserOut_class)
async def create_user(user_in: UserIn_class):
    user_saved = fake_save_user(user_in)
    return user_saved



class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

# 可以用union响应两种类型，详细的放前面
@app.get("/unions/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

# 还可以响应 lst
@app.get("/lst/", response_model=List[Item])
async def read_items():
    return items

# [
#   {
#     "name": "Foo",
#     "description": "There comes my hero"
#   },
#   {
#     "name": "Red",
#     "description": "It's my aeroplane"
#   }
# ]


# 你还可以使用一个任意的普通 dict 声明响应，
# 仅声明键和值的类型，而不使用 Pydantic 模型。
# 如果你事先不知道有效的字段/属性名称（对于 Pydantic 模型是必需的），这将很有用。
# 响应dct
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}


# 响应码
# fastapi.status有定义
# @app.post("/status_code/", status_code=201)
# 你也可以使用 from starlette import status。
# 为了给你（即开发者）提供方便，
# FastAPI 提供了与 starlette.status 完全相同的 fastapi.status。
# 但它直接来自于 Starlette。
@app.post("/status_code/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


##################################################################
# 表单 form















# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_extra_models:app', host="127.0.0.1", port=1902, reload=True, debug=True)

