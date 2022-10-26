import os

import uvicorn

from fastapi import FastAPI


# 元数据和文档 URL ? 什么玩意
# OpenAPI 好像就是swagger前身 这章是写文档？

# Title：在 OpenAPI 和自动 API 文档用户界面中作为 API 的标题/名称使用。
# Description：在 OpenAPI 和自动 API 文档用户界面中用作 API 的描述。
# Version：API 版本，例如 v2 或者 2.5.0。

# md 格式
description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


app = FastAPI(
    title="ChimichangApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    # 文档位置
    # docs_url="/documentation", 
    # 另一个文档类型
    # redoc_url=None,
)


# @app.get("/items/")
# async def read_items():
#     return [{"name": "Katana"}]


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]







# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)