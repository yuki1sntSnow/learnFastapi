from enum import Enum
from typing import Union, Optional, List

import uvicorn

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


app = FastAPI()


@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 3.10 + 
@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 导入Query 添加校验
# @app.get("/querys/")
# async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


@app.get("/querys/")
async def read_items(
    q: Union[str, None] = Query(default=None, min_length=3, max_length=50)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# regex
@app.get("/regex/")
async def read_items(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, regex="^fixedquery$"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# q 的默认值 default="fixedquery"
@app.get("/default/")
async def read_items(q: str = Query(default="fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# ellipsis ... 省略号 声明q的值是必须的 required
@app.get("/ellipsis/")
async def read_items(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# http://localhost:1902/lists/?q=foo&q=bar
# list 多个值
@app.get("/lists/")
async def read_items(q: Union[List[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items

# 这么写 不会检查列表内容
@app.get("/test1/")
async def read_items(q: list = Query(default=[])):
    query_items = {"q": q}
    return query_items

# 没有这种写法
# @app.get("/test2/")
# async def read_items(q: list = Query(default=[int])):
#     query_items = {"q": q}
#     return query_items

# 可以限定 list 中是 int
@app.get("/test3/")
async def read_items(q: list[int] = Query(default=[])):
    query_items = {"q": q}
    return query_items


@app.get("/title/")
async def read_items(
    q: Union[str, None] = Query(default=None, title="Query string", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/description/")
async def read_items(
    q: str
    | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 别名 item-query 替换 q
# http://localhost:1902/alias/?item-query=foobaritems
@app.get("/alias/")
async def read_items(q: str | None = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 弃用 deprecated 能用但是文档里会显示
@app.get("/deprecated/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 查询参数和字符串校验 Query
##################################################
# 路径参数和数值校验 Path

@app.get("/path/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 用法和query差不多，path是必须的，无论是否为None
@app.get("/default/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 不需要考虑参数的位置关系
@app.get("/sort/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# kwargs用法
# 如果你想不使用 Query 声明 没有默认值的查询参数 q，
# 同时使用 Path 声明路径参数 item_id，并使它们的顺序与上面不同，
# Python 对此有一些特殊的语法。传递 * 作为函数的第一个参数。
# Python 不会对该 * 做任何事情，
# 但是它将知道之后的所有参数都应作为关键字参数（键值对），
# 也被称为 kwargs，来调用。即使它们没有默认值。
@app.get("/kwargs/{item_id}")
# 用* 能解决顺序问题
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
# 会报错 顺序问题
# async def read_items(item_id: int = Path(title="The ID of the item to get"), q: str):
# 正常
# async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 大于小于等于
# ge=1 greater than & equal  ge >= 1
@app.get("/greater/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# gt=0 greater than   gt > 0
# le=1000 less than & equal  le <= 1000
@app.get("/less/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# float
@app.get("/float/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



#################################################
# put
















    
# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_queryValidation:app', host="127.0.0.1", port=1902, reload=True, debug=True)
