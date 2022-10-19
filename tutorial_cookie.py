from tkinter.messagebox import NO
from typing import Union, List

import uvicorn

from fastapi import Cookie, FastAPI, Header
from pydantic import BaseModel, EmailStr



app = FastAPI()


# Cookie 、Path 、Query是兄弟类，它们都继承自公共的 Param 类
# 但请记住，当你从 fastapi 导入的 Query、Path、Cookie 或其他参数声明函数，这些实际上是返回特殊类的函数。
# 你需要使用 Cookie 来声明 cookie 参数，否则参数将会被解释为查询参数。

@app.get("/cookie/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}


# cookie 
# ?? 好吧 就是教调接口.... 
# 文件名字懒得改了 x
############################################################3
#header


@app.get("/header/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}



# 去重
@app.get("/x_token/")
async def read_items(x_token: List[str] | None = Header(default=None)):
    return {"X-Token values": x_token}


# header 也是介绍接口
##########################################################
# response_model
# @app.get()
# @app.post()
# @app.put()
# @app.delete()
# 等等。


class response_model(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


# 注意，response_model是「装饰器」方法（get，post 等）的一个参数。
# 不像之前的所有参数和请求体，它不属于路径操作函数。
@app.post("/response_model/", response_model=response_model)
async def create_item(item: response_model):
    return item



class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


# Don't do this in production!
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


# 能过滤掉密码
# FastAPI 将会负责过滤掉未在输出模型中声明的所有数据（使用 Pydantic）
@app.post("/UserOut/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# response_model_exclude_unset
# 字面意思 过滤默认值
class response_model_exclude_unset(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# 但是依然建议使用多个类而不是这些参数。
# 这是因为即使使用 response_model_include 或 response_model_exclude 来省略某些属性，
# 在应用程序的 OpenAPI 定义（和文档）中生成的 JSON Schema 仍将是完整的模型。
# 这也适用于作用类似的 response_model_by_alias。
@app.get("/items_s/{item_id}", response_model=response_model_exclude_unset, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]



class response_model_exclude(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

# {"name", "description"} 语法创建一个具有这两个值的 set。
# 等同于 set(["name", "description"])。
@app.get(
    "/response_model_exclude/{item_id}/name",
    response_model=response_model_exclude,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/response_model_exclude/{item_id}/public", response_model=response_model_exclude, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]



# 如果你忘记使用 set 而是使用 list 或 tuple，FastAPI 仍会将其转换为 set 并且正常工作：
@app.get(
    "/list/{item_id}/name",
    response_model=response_model_exclude,
    # 这里
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/list/{item_id}/public", response_model=response_model_exclude, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]





# 使用路径操作装饰器的 response_model 参数来定义响应模型，特别是确保私有数据被过滤掉。

# 使用 response_model_exclude_unset 来仅返回显式设定的值。
# 推荐 再写一个响应模型


#分p 问就是我也不知道为啥.jpg
#############################################################################




# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_cookie:app', host="127.0.0.1", port=1902, reload=True, debug=True)
