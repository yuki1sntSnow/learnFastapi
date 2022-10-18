from enum import Enum
from typing import Union
from typing import Optional

import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

# 继承BaseModel
# name和price 没赋值默认为必须
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    # tax: Union[float, None] = None
    tax: Optional[float] = None


app_post = FastAPI()

# 查询 get end
###################################################
# 请求体 post 

@app_post.post("/items/")
async def create_item(item: Item):
    return item


@app_post.post("/uses/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# put 请求体 + 路径参数
@app_post.put("/put/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# 请求体 + 路径参数 + 查询参数

# 函数参数将依次按如下规则进行识别：

# 如果在路径中也声明了该参数，它将被用作路径参数。 
# item_id
# 如果参数属于单一类型（比如 int、float、str、bool 等）它将被解释为查询参数。
# q
# 如果参数的类型被声明为一个 Pydantic 模型，它将被解释为请求体。
# item
@app_post.put("/puts/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# 请求体
#################################################################
# 查询参数和字符串校验





















# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_post:app_post', host="127.0.0.1", port=1902, reload=True, debug=True)
