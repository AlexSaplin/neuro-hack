from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from common.config import config

BaseUsers = declarative_base()


class UserMeta(BaseUsers):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    token = Column(String, nullable=False)


class TaskMeta(BaseUsers):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    author_id = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)


class TaskUserMeta(BaseUsers):
    __tablename__ = 'tasks_user'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    results = Column(String)

