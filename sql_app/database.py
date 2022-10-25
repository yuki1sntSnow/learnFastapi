from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# pip install sqlalchemy

# .
# └── sql_app
#     ├── __init__.py
#     ├── crud.py
#     ├── database.py
#     ├── main.py
#     ├── models.py
#     └── schemas.py


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    # 这句话只适用于sqlite 其他的db不需要
    # SQLite只允许一个线程与之通信
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


