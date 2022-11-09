from dataclasses import dataclass, field
from typing import Union, List

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item


@dataclass
class Item2:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None



@app.get("/items/next", response_model=Item2)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be be playin' and havin' fun",
        "tags": ["breater"],
    }



# uvicorn tutorial:app --port 1902 --reload --debug
if __name__ == '__main__':
    import os, uvicorn
    # uvicorn.run(app='tutorial_DependencyInjection:app_global', host="127.0.0.1", port=1902, reload=True, debug=True)
    filename = os.path.basename(__file__)
    filename = filename[:-3]
    uvicorn.run(app=filename+':app', host="127.0.0.1", port=1902, reload=True, debug=True)
