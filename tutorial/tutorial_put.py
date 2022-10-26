import imp


import os
from typing import Union, List, Set, Dict
from datetime import datetime, time, timedelta
# uuid竟然是官方库 x
from uuid import UUID

import uvicorn

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


# 3.6+
# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: Union[float, None] = None


# 3.10+
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None



# item: Item | None = None,
# item 变为可选
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results



@app.put("/multi/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.put("/body/{item_id}")
async def update_item(
    item_id: int, 
    item: Item, 
    user: User, 
    importance: int = Body()
):
    results = {
        "item_id": item_id, 
        "item": item, 
        "user": user, 
        "importance": importance
    }
    return results

# body test
# 不用Body(), 会变成查询 在urls里 不进body
@app.put("/body_test/{item_id}")
async def update_item(
    item_id: int, 
    item: Item, 
    user: User, 
    importance: int
):
    results = {
        "item_id": item_id, 
        "item": item, 
        "user": user, 
        "importance": importance
    }
    return results

# '{
#   "item": {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "tax": 0
#   },
#   "user": {
#     "username": "string",
#     "full_name": "string"
#   },
#   "importance": 0
# }'

# 区别在 importance 在查询还是body
# test
# 'http://127.0.0.1:1902/body_test/1?importance=2'
# '{
#   "item": {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "tax": 0
#   },
#   "user": {
#     "username": "string",
#     "full_name": "string"
#   }
# }'


# importance 这里Body()和其他的一样，能做限制。
@app.put("/importance/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# embed
@app.put("/embed/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# embed
# '{
#   "item": {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "tax": 0
#   }
# }'


@app.put("/noEmbed/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# '{
#   "name": "string",
#   "description": "string",
#   "price": 0,
#   "tax": 0
# }'


###############################################################
# Field 请求体 字段 pydantic 库的？
# from pydantic import BaseModel, Field

# 实际上，Query、Path 和其他你将在之后看到的类，
# 创建的是由一个共同的 Params 类派生的子类的对象，
# 该共同类本身又是 Pydantic 的 FieldInfo 类的子类
# json schemas 能看到 description
class Item_field(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/Field/{item_id}")
async def update_item(item_id: int, item: Item_field = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


##########################################################
# 请求体 - 嵌套模型



# tags = []
class Item_list(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = []


@app.put("/Item_list/{item_id}")
async def update_item(item_id: int, item: Item_list):
    results = {"item_id": item_id, "item": item}
    return results

# tags 
class Item_list_str(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.put("/Item_list_str/{item_id}")
async def update_item(item_id: int, item: Item_list_str):
    results = {"item_id": item_id, "item": item}
    return results

# {
#   "item_id": 1,
#   "item": {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "tax": 0,
#     "tags": [
#       "1",
#       "2",
#       "a",
#       "13r4t5",
#       "342.rwe"
#     ]
#   }
# }


# 封装了set 可以过滤
class Item_set(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.put("/Item_set/{item_id}")
async def update_item(item_id: int, item: Item_set):
    results = {"item_id": item_id, "item": item}
    return results



# 嵌套
class Image(BaseModel):
    url: str
    name: str


class Item_image(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None


@app.put("/images/{item_id}")
async def update_item(item_id: int, item: Item_image):
    results = {"item_id": item_id, "item": item}
    return results


# HttpUrl 该字符串将被检查是否为有效的 URL，并在 JSON Schema / OpenAPI 文档中进行记录。
class Image_HttpUrl(BaseModel):
    url: HttpUrl
    name: str


class Item_image_HttpUrl(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image_HttpUrl, None] = None


@app.put("/Item_image_HttpUrl/{item_id}")
async def update_item(item_id: int, item: Item_image_HttpUrl):
    results = {"item_id": item_id, "item": item}
    return results


# 反正就是各种嵌套
class Image_t(BaseModel):
    url: HttpUrl
    name: str


class Item_t(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image_t], None] = None


@app.put("/item_t/{item_id}")
async def update_item(item_id: int, item: Item_t):
    results = {"item_id": item_id, "item": item}
    return results

# '{
#   "name": "string",
#   "description": "string",
#   "price": 0,
#   "tax": 0,
#   "tags": [],
#   "images": [
#     {
#       "url": "http://127.0.0.1",
#       "name": "string"
#     },
#     {
#       "url": "http://127.0.0.1",
#       "name": "2"
#     }
#   ]
# }'


# 三层
class Image_xjbt(BaseModel):
    url: HttpUrl
    name: str


class Item_xjbt(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image_xjbt], None] = None


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item_xjbt]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# '{
#   "name": "string",
#   "description": "string",
#   "price": 0,
#   "items": [
#     {
#       "name": "string",
#       "description": "string",
#       "price": 0,
#       "tax": 0,
#       "tags": ["a", "b", "c"],
#       "images": [
#         {
#           "url": "http://127.0.0.1:1902/offers/",
#           "name": "string"
#         }
#       ]
#     }
#   ]
# }'


# 包一层List[] {} 变成 []
@app.post("/request_list/")
async def create_multiple_images(images: List[Image]):
    return images


# dct
# 请记住 JSON 仅支持将 str 作为键。
# 但是 Pydantic 具有自动转换数据的功能。
# 这意味着，即使你的 API 客户端只能将字符串作为键发送，
# 只要这些字符串内容仅包含整数，Pydantic 就会对其进行转换并校验。
# 然后你接收的名为 weights 的 dict 实际上将具有 int 类型的键和 float 类型的值。
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

# {
#   "1": 0.1,
#   "2": 20,
#   "4": 9.1
# }



# 模式的额外信息 - 例子
# example: OrderedMap { "name": "Foo", "description": "A very nice Item", "price": 35.4, "tax": 3.2 }
class Item_schema_extra(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items_schema_extra/{item_id}")
async def update_item(item_id: int, item: Item_schema_extra):
    results = {"item_id": item_id, "item": item}
    return results



# 请记住，传递的那些额外参数不会添加任何验证，只会添加注释，用于文档的目的。
class Item_example(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)


@app.put("/items_example/{item_id}")
async def update_item(item_id: int, item: Item_example):
    results = {"item_id": item_id, "item": item}
    return results

# Item_example{
# name*	string
# title: Name
# example: Foo
# description	string
# title: Description
# example: A very nice Item
# price*	number
# title: Price
# example: 35.4
# tax	number
# title: Tax
# example: 3.2
 
# }



# 其他数据类型

# UUID:
# 一种标准的 "通用唯一标识符" ，在许多数据库和系统中用作ID。
# 在请求和响应中将以 str 表示。

# datetime.datetime:
# 一个 Python datetime.datetime.
# 在请求和响应中将表示为 ISO 8601 格式的 str ，比如: 2008-09-15T15:53:00+05:00.

# datetime.date:
# Python datetime.date.
# 在请求和响应中将表示为 ISO 8601 格式的 str ，比如: 2008-09-15.

# datetime.time:
# 一个 Python datetime.time.
# 在请求和响应中将表示为 ISO 8601 格式的 str ，比如: 14:23:55.003.

# datetime.timedelta:
# 一个 Python datetime.timedelta.
# 在请求和响应中将表示为 float 代表总秒数。
# Pydantic 也允许将其表示为 "ISO 8601 时间差异编码"

# 这个没太懂 不重要（
# frozenset:
# 在请求和响应中，作为 set 对待：
# 在请求中，列表将被读取，消除重复，并将其转换为一个 set。
# 在响应中 set 将被转换为 list 。
# 产生的模式将指定那些 set 的值是唯一的 (使用 JSON 模式的 uniqueItems)。

# bytes:
# 标准的 Python bytes。
# 在请求和相应中被当作 str 处理。
# 生成的模式将指定这个 str 是 binary "格式"。

# Decimal:
# 标准的 Python Decimal。
# 在请求和相应中被当做 float 一样处理。
# 您可以在这里检查所有有效的pydantic数据类型: Pydantic data types.
# https://pydantic-docs.helpmanual.io/usage/types/



# uuid 格式 (8-4-4-4-12)
# a8098c1a-f86e-11da-bd1a-00112444be1e
# time: 04:23:01+04:00
@app.put("/items_uuid")
async def read_items(
    item_id: UUID | None = None,
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None),
):
    # 这块是原生 加减
    start_process = start_datetime + process_after
    duration = end_datetime - start_process

    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }













# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(filename)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)