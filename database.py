from sqlmodel import create_engine, SQLModel, Session
import os

# 数据库文件名为 storage.db
sqlite_file_name = "storage.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args={"check_same_thread": False} 是 SQLite 必须的配置
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    # 这一步会根据 models.py 中的 table=True 自动创建表
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session