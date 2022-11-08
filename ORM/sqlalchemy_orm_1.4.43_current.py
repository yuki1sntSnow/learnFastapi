from sqlalchemy import create_engine

from sqlalchemy.orm import Session

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import select

from sqlalchemy.types import DateTime

Base = declarative_base()


# CREATE TABLE `y_user`  (
#   `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键id',
#   `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '登录名，限20字',
#   `pass` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '密码，限20字',
#   `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最近更新时间',
#   PRIMARY KEY (`id`) USING BTREE
# ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;




class y_user(Base):
    __tablename__ = 'y_user'
    id = Column(Integer, primary_key=True, comment='主键id')
    name = Column(String(20), comment='登录名，限20字')
    password = Column(String(20), comment='密码，限20字')
    create_time = Column(DateTime(), comment='创建时间')
    update_time = Column((), comment='最近更新时间')
    __table_args__ = ({'comment': '用户表'})  

    # 添加索引和表注释
    # __table_args__ = (Index('index(zone,status)', 'resource_zone', 'resource_status'), {'comment': '用户表'})  

class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

print('----------------------------------------------------------------')

engine = create_engine("sqlite:///ORM/test.db", echo=True, future=True)
Base.metadata.create_all(engine)

print('----------------------------------------------------------------')

with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()

print('----------------------------------------------------------------')

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(user)





