from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

Base = declarative_base()


# CREATE TABLE `y_user`  (
#   `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键id',
#   `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '登录名，限20字',
#   `pass` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '密码，限20字',
#   `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最近更新时间',
#   PRIMARY KEY (`id`) USING BTREE
# ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

# 一个字符串格式？ 另一个引擎啥的 和 row_format 不知道是啥的 能用orm创建吗？
# SET utf8mb4 COLLATE utf8mb4_general_ci 
# ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic
class y_user(Base):
    __tablename__ = 'y_user'
    id = Column(Integer, primary_key=True, nullable=False, comment='主键id')
    name = Column(String(20), nullable=False, comment='登录名，限20字')
    password = Column(String(20), nullable=False, comment='密码，限20字')
    create_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='最近更新时间')
    __table_args__ = ({'comment': '用户表'})  

    # 添加索引和表注释
    # __table_args__ = (Index('index(zone,status)', 'resource_zone', 'resource_status'), {'comment': '用户表'})  
engine = create_engine("sqlite:///ORM/kirito.db", echo=True, future=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    
    # test = y_user(
    #     name='test',
    #     password='',
    # )
    # session.add(test)
    # session.commit()
    session.query(y_user).filter_by(id=3).update({y_user.password:'3333'})
    session.commit()
