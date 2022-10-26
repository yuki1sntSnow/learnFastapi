from typing import Set, Union, List
from datetime import datetime

import uvicorn

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


# 路径操作装饰器支持多种配置参数。
# 注意：以下参数应直接传递给路径操作装饰器，不能传递给路径操作函数。
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


# status_code 用于定义路径操作响应中的 HTTP 状态码。
# 可以直接传递 int 代码， 比如 404。
# 如果记不住数字码的涵义，也可以用 status 的快捷常量
@app.post("/status_code/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item


# tags 用于为路径操作添加标签
# OpenAPI 概图会自动添加标签，供 API 文档接口使用：
# 好像是为了文档的参数
@app.post("/itemsp/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/itemsp/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


# 文档字符串（docstring）
# 描述内容比较长且占用多行时，可以在函数的 docstring 中声明路径操作的描述，
# FastAPI 支持从文档字符串中读取描述内容。
# 文档字符串支持 Markdown，能正确解析和显示 Markdown 的内容，但要注意文档字符串的缩进。
@app.post("/docstring/", response_model=Item, summary="Create an item 111", tags=["12"])
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


# 注意，response_description 只用于描述响应，description 一般则用于描述路径操作。
# OpenAPI 规定每个路径操作都要有响应描述。
# 如果没有定义响应描述，FastAPI 则自动生成内容为 "Successful response" 的响应描述。
@app.post(
    "/response_description/",
    response_model=Item,
    summary="Create an item SSS",
    response_description="The created item @@@",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


# 弃用路径操作
# deprecated 参数可以把路径操作标记为弃用，无需直接删除：
# 文档里变灰
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]



# 这里的参数好像都是给人看的
# 可有可无.jpg？
########################################################################3
# JSON 兼容编码器


fake_db = {}

class Item_jsonable_encoder(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.put("/jsonable_encoder1/{id}")
def update_item(id: str, item: Item_jsonable_encoder):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    # return fake_db

# 在这个例子中，它将Pydantic模型转换为dict，并将datetime转换为str。
# 调用它的结果后就可以使用Python标准编码中的json.dumps()。
# 这个操作不会返回一个包含JSON格式（作为字符串）数据的庞大的str。
# 它将返回一个Python标准数据结构（例如dict），其值和子值都与JSON兼容。


####################################################################################################
# 请求体 - 更新数据
# 用 PUT 更新数据


class Itemxx(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


# 用 PUT 把数据项 bar 更新为以下内容时
# 因为上述数据未包含已存储的属性 "tax": 20.2，新的输入模型会把 "tax": 10.5 作为默认值。
# 因此，本次操作把 tax 的值「更新」为 10.5。
itemsxx = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Itemxx)
async def read_item(item_id: str):
    return itemsxx[item_id]

# PUT 用于接收替换现有数据的数据
@app.put("/items/{item_id}", response_model=Itemxx)
async def update_item(item_id: str, item: Itemxx):
    update_item_encoded = jsonable_encoder(item)
    itemsxx[item_id] = update_item_encoded
    return update_item_encoded


# PATCH 没有 PUT 知名，也怎么不常用。
# 很多人甚至只用 PUT 实现部分更新。
# FastAPI 对此没有任何限制，可以随意互换使用这两种操作。
# 但本指南也会分别介绍这两种操作各自的用途。
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = itemsxx[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    itemsxx[item_id] = jsonable_encoder(updated_item)
    return updated_item


# 实际上，HTTP PUT 也可以完成相同的操作。 但本节以 PATCH 为例的原因是，该操作就是为了这种用例创建的。






# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_PathOperationConfiguration:app', host="127.0.0.1", port=1902, reload=True, debug=True)

