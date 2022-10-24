import os
import uvicorn

from enum import Enum
from typing import Union

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# uvicorn tutorial:my_awesome_api --port 1902 --reload
# my_awesome_api = FastAPI()


# @my_awesome_api.get("/")
# async def root():
#     return {"message": "Hello World"}


# uvicorn tutorial:app --port 1902 --reload
app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
# async def read_item(item_id):
async def read_item(item_id: int):
    return {"item_id": item_id}


# 顺序问题 会导致/users/me返回的优先级
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# 枚举 声明路径参数
@app.get("/models/{model_name}")
# model_name: ModelName 限定ModelName类
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# 如果file_path带/ 会出现// 注意点 本质还是str
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 查询字符串是键值对的集合，这些键值对位于 URL 的 ？ 之后，并以 & 符号分隔
@app.get("/items/")
# skip和limit原始值是str, :int 类型校验, 
# =0 =10 是默认值, 
# http://127.0.0.1:8000/items/ == http://127.0.0.1:1902/items/?skip=0&limit=10
#
# http://127.0.0.1:8000/items/?skip=20
# skip = 20, limit = 10, 默认值
async def read_item(skip: int = 0, limit: int = 10):
    # 这是个list切片操作
    return fake_items_db[skip : skip + limit]


# http://127.0.0.1:1902/union/foo?q=bar
# @app.get("/union/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

# http://127.0.0.1:1902/union/1?q=bar&short=true
@app.get("/union/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# 不添加内容，就是必须的参数
@app.get("/musts/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# needy，一个必需的 str 类型参数。
# skip，一个默认值为 0 的 int 类型参数。
# limit，一个可选的 int 类型参数。
# item_id是路径，参数里面和needy一样是必须的，skip预设0，limit预设None且需要int
# http://127.0.0.1:1902/parameters/1?needy=2&skip=3&limit=5
# "type":"type_error.integer"
@app.get("/parameters/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[list, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# 查询 get end
###################################################
# 请求体 post 







# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)