from fastapi import FastAPI

app = FastAPI()

items = {}


# @app.on_event("startup")
# async def startup_event():
#     items["foo"] = {"name": "Fighters"}
#     items["bar"] = {"name": "Tenders"}


# @app.get("/items/{item_id}")
# async def read_items(item_id: str):
#     return items[item_id]

# i/o 要等待 没加async
@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items2/")
async def read_items():
    return [{"name": "Foo"}]


# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    import os, uvicorn

    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)