import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    import os, uvicorn
    # uvicorn.run(app='tutorial_DependencyInjection:app_global', host="127.0.0.1", port=1902, reload=True, debug=True)
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)
