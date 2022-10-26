from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# "/static" 子程序将被挂载到的子路径。任何以"/static" 开头的路径都将被它处理。
# directory="static" 包含你的静态文件的目录名称。
# name="static" 给它一个可以被FastAPI内部使用的名字。
# https://www.starlette.io/staticfiles/
app.mount("/static", StaticFiles(directory="static"), name="static")
