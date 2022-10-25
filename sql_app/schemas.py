from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None

# 和fastapi链接用的入口，多包装了一层
class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

# 和fastapi链接用的入口，多包装了一层 同理
class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
