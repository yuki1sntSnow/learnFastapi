```
pip install sqlalchemy
```
...

```
.
└── sql_app
    ├── __init__.py # empty
    ├── crud.py # 用orm操作db，也是封装一堆函数，需要学SQLAlchemy语句
    ├── database.py # SQLAlchemy engine
    ├── main.py # fastapi
    ├── models.py # SQLAlchemy models
    └── schemas.py # Pydantic models / schemas

```
### style 

SQLAlchemy

```
name = Column(String)
```

Pydantic 

```
name: str
```
感觉容易写乱.jpg

Alembic 数据库迁移工具 建表

好像是因为SQLAlchemy的原因 fastapi没用异步，具体咋改也有办法，有机会再看。

celery rq arq 基于分布式消息传递的开源异步任务队列或作业队列？ 我大概率一时半会用不上
