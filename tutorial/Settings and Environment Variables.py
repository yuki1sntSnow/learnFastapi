from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    import os, uvicorn

    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)