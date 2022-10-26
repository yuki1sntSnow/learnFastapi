# 包的结构问题的莫名其妙解决方案... 
# 用sys.path.append()
# 配合绝对路径 .module 还不行...
# https://stackoverflow.com/questions/16981921

import os, sys
import uvicorn

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from fastapi import Depends, FastAPI

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
# from .routers import items, users

from app.dependencies import get_query_token, get_token_header
from app.internal import admin
from app.routers import items, users


app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# 用 __main__ 有个路径问题 直接在控制台搞了.jpg
# uvicorn app.main:app --port 1902 --reload --debug

if __name__ == '__main__':    
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)

