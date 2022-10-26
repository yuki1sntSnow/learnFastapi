# 测试单元？
# To use TestClient, first install requests.
# pip install requests
# Create functions with a name that starts with test_ (this is standard pytest conventions).

# pip install pytest
# 能自动索敌.jpg test_开头的文件

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

