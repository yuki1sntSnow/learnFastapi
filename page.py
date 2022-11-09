from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

from pydantic import BaseModel


app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.post("/form", response_class=HTMLResponse)
async def form_test(response: Response, name: str = Form(), password: str = Form()):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    response.set_cookie(key="111", value="222")

    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Cookies</h1>
        </body>
    </html>
    """

# uvicorn page:app --port 1902 --reload --debug
