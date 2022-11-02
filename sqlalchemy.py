from sqlalchemy import create_engine
from sqlalchemy import text

from sqlalchemy.orm import Session

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey

# 1.4 新特性 registry.generate_base() 取代 declarative_base()
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from sqlalchemy import insert

# 现在1.4好像是为了2.0的过渡版本，废弃掉以前的不少语句，然后还有迁移啥的？ 不是很懂
# 分为 core层和 orm层？ 好像一个是直接写sql的意思

# 临时数据库 :memory:
# engine = create_engine("sqlite:///:memory:", echo=True, future=True)

# 创建一个 SQLite 的内存数据库
engine = create_engine("sqlite:///:memory:", 
    echo=True, # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
    future=True, # 使用 SQLAlchemy 2.0 API，向后兼容
    connect_args={"check_same_thread": False} # 必须加上 check_same_thread=False，否则无法在多线程中使用
)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
    
    print('-------------------------------------')
    
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()

print('-------------------------------------')
# 新写法 begin
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
        )

print('-------------------------------------')

with engine.connect() as conn:
    result = conn.execute(text("select x, y from some_table"))
    for row in result:
        print(f'x: {row.x} y: {row.y}')

#
# # Tuple 
# result = conn.execute(text("select x, y from some_table"))
# for x, y in result:
#     pass

# # Integer 
# result = conn.execute(text("select x, y from some_table"))
# for row in result:
#     x = row[0]
#     pass

# # Attribute 
# result = conn.execute(text("select x, y from some_table"))
# for row in result:
#     y = row.y
#     print(f"Row: {row.x} {y}")

# # Mapping
# result = conn.execute(text("select x, y from some_table"))
# for dict_row in result.mappings():
#     x = dict_row["x"]
#     y = dict_row["y"]
#

print('-------------------------------------')

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT x, y FROM some_table WHERE y > :a"),
        {"a": 5}
    )
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

print('-------------------------------------')

with engine.connect() as conn:
    conn.execute(
    text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
    [{"x": 11, "y": 12}, {"x": 13, "y": 14}]
    )
    conn.commit()

print('-------------------------------------')

# bindparams 给个参数
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

print('-----------session--------------------------')

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=10)
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

print('-------------------------------------')

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y":11}, {"x": 13, "y": 15}]
    )
    session.commit()

print('--------------MetaData--建表---------------------')

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)

print(user_table.c.id)
print(user_table.c.keys())
print(user_table.primary_key)

print('-------------------------------------')

address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

print('-------------registry------------------------')

metadata_obj.create_all(engine)

mapper_registry = registry()

print(mapper_registry.metadata)

Base = mapper_registry.generate_base()

mapper_registry = registry()

# Base = mapper_registry.generate_base()

# class MyClass(Base):
#     __tablename__ = "my_table"
#     id = Column(Integer, primary_key=True)

##################################################
# mapper_registry = registry()

# class Base(metaclass=DeclarativeMeta):
#     __abstract__ = True
#     registry = mapper_registry
#     metadata = mapper_registry.metadata

#     __init__ = mapper_registry.constructor

# 这种映射写法 好像是最常用的？ 
# 声明性映射？

class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    
    addresses = relationship("Address", back_populates="user")
    
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
 
class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")
    
    # 可选的看返回
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

print(User.__table__)

sandy = User(name="sandy", fullname="Sandy Cheeks")

print(sandy)

print('-------------------------------------')

some_table = Table("some_table", metadata_obj, autoload_with=engine)

print('-------------------------------------')

# 好像不推荐这种写法 不是orm
stmt = insert(user_table).values(name='spongebob', fullname="Spongebob Squarepants")

print(stmt)

compiled = stmt.compile()

print(compiled.params)

print('-------------------------------------')

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

print(result.inserted_primary_key)


print('-------------------------------------')

# 好像学错了.jpg
# 还没到如何用orm...
# 这个core，好像就是如何转换成sql语句

# 以及 orm 应该是两个作用？
# 1. 做映射 类 和 表
# 2. 转译 py语句 到 sql语句
# 不知道理解的对不对.jpg