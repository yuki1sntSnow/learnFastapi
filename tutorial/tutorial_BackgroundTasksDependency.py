import os

import uvicorn

# 加了依赖注入
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


# 这个操作类似手动记录日志了？
def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


# 加了个查询q，先走这个q的依赖的写入
@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

# 短时间应该不用学 x
# 如果需要进行繁重的后台计算，而且不一定需要由同一个进程来实现（例如，你不需要共享内存、变量等），
# 你比如Celery （异步的框架？）
# 配置更复杂，消息队列 如RabbitMQ或Redis，允许在多个进程中运行后台任务，特别是在多个服务器中
# 简单的后台任务可以用 BackgroundTasks


# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)