import uvicorn

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# 复用 FastAPI 异常处理器
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        # 因为是 Python 异常，所以不能 return，只能 raise。
        # 触发 HTTPException 时，可以用参数 detail 传递任何能转换为 JSON 的值，不仅限于 str。
        # 还支持传递 dict、list 等数据结构。
        # FastAPI 能自动处理这些数据，并将之转换为 JSON。
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


# 自定义响应头
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


# 安装自定义异常处理器
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# 覆盖默认异常处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/HTTPExceptions/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}



# 复用 FastAPI 异常处理器
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items5/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}



#######################################
# 最后这几个异常的没细看，用到的时候再说。










# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_handling_errors:app', host="127.0.0.1", port=1902, reload=True, debug=True)

