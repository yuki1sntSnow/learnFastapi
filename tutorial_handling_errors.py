import uvicorn

from fastapi import FastAPI, HTTPException

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


########################################################################
# 明天再说.jpg 
# 安装自定义异常处理器




# ps 用这个的目的单纯是1902（

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    uvicorn.run(app='tutorial_handling_errors:app', host="127.0.0.1", port=1902, reload=True, debug=True)

