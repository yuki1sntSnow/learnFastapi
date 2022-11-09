from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# 限制https
app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# from fastapi import FastAPI
# from fastapi.middleware.trustedhost import TrustedHostMiddleware

# app = FastAPI()

# 限制host
# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
# )


# @app.get("/")
# async def main():
#     return {"message": "Hello World"}


# from fastapi import FastAPI
# from fastapi.middleware.gzip import GZipMiddleware

# app = FastAPI()

# ？
# app.add_middleware(GZipMiddleware, minimum_size=1000)


# @app.get("/")
# async def main():
#     return "somebigcontent"


# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    import os, uvicorn

    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)