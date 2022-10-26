import imp
from typing import Union

import os
import uvicorn

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

# 开始学习我完全不理解的东西了 x
######################################################################################
# 底层原理不同，但是这玩意不就是调接口嘛。。。用Depends()（还搞了个新名词 x
# 和定义类调用一样，注入是定义函数，然后用框架包装好的方法

# 其他与「依赖注入」概念相同的术语为：
# 资源（Resource）
# 提供方（Provider）
# 服务（Service）
# 可注入（Injectable）
# 组件（Component）

# 看图好理解
# FastAPI 兼容性
# https://fastapi.tiangolo.com/zh/tutorial/dependencies/

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




# 下一章将详细介绍在关系型数据库、NoSQL 数据库、安全等方面使用依赖项的例子。
######################################################################################
# Classes as Dependencies
# 这章没汉化（我发现日语版本地化更差） 可恶啊 搞得我都想翻译一波了 x 
# 如果学完感觉不错的话 考虑在社区贡献一波.jpg？
# 不过本地化不是刚需吧（这又不是二刺螈追番 谁都来看，写代码的还看文档的多多少少都会点英语吧... x


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# Classes as dependencies
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items_class/")
# 这里第一个 CommonQueryParams 可以省略 啥也没做
# 但是推荐写上能做代码补全
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
# async def read_items(commons=Depends(CommonQueryParams)):
# sortcut 能这样省略..
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# 子依赖项 
# 就是层层嵌套的函数 然后拿返回值。。。
def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q


@app.get("/items_sub/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}



# FastAPI 不会为同一个请求多次调用同一个依赖项，
# 而是把依赖项的返回值进行「缓存」，并把它传递给同一请求中所有需要使用该返回值的「依赖项」。
# 在高级使用场景中，如果不想使用「缓存」值，
# 而是为需要在同一请求的每一步操作（多次）中都实际调用依赖项，
# 可以把 Depends 的参数 use_cache 的值设置为 False

# async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
#     return {"fresh_value": fresh_value}

##############

# 路径操作装饰器依赖项
# Dependencies in path operation decorators
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items_path/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


# Global Dependencies
app_global = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app_global.get("/items_global/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app_global.get("/users_global/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


# 接下来的内容 基本上一知半解 不知道有啥用.jpg 
# 主要是py的 yield用的少
# 还有这个抛异常图个啥.jpg 自定义异常啥的
# Dependencies with yield
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()


# For example, dependency_c can have a dependency on dependency_b, 
# and dependency_b on dependency_a
async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)

# yield 之前能抛异常
# yield 之后异常会被吞

class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db






















# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    # uvicorn.run(app='tutorial_DependencyInjection:app_global', host="127.0.0.1", port=1902, reload=True, debug=True)
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)
