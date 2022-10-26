import imp
import time
import os

import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # 请记住可以 用'X-' 前缀添加专有自定义请求头
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 中间件好像就告诉你怎么调用了 具体没讲 =，=
# 反正就是个第三方的函数 X入
###############################################################################3
# CORS（跨域资源共享）


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:1903",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}








# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)


    # uvicorn.run("main:app", port=443, host='0.0.0.0', reload = True, reload_dirs = ["html_files"], ssl_keyfile="/etc/letsencrypt/live/my_domain/privkey.pem", ssl_certfile="/etc/letsencrypt/live/my_domain/fullchain.pem")
