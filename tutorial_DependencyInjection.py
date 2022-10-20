from typing import Union

import uvicorn

from fastapi import Depends, FastAPI

app = FastAPI()

# 开始学习我完全不理解的东西了 x
#########################################

async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons






















# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_DependencyInjection:app', host="127.0.0.1", port=1902, reload=True, debug=True)

