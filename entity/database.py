from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .models import Base

# 数据库主机
DB_HOST = '114.55.91.77'
# 数据库端口
DB_PORT = 3306
# 数据库用户名
DB_USERNAME = 'root'
# 数据库密码
DB_PASSWORD = 'RJyRZQP6QTcf6k7M'
# 数据库名称
DB_DATABASE = 'SQLAlchemy'

# 数据库配置
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
engine = create_engine(DATABASE_URL, echo=True,
                       pool_pre_ping=True, pool_recycle=3600)


def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(engine)


def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session
