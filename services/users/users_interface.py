from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.config import config
from services.users.models import BaseUsers, UserMeta, TaskMeta, TaskUserMeta
from models import BaseUsers, UserMeta, TaskMeta, TaskUserMeta
from services.archangel.API import API


class UsersInterface:
    def __init__(self):
        self.engine = create_engine(config.DB_USERS_URL)
        self.sessionmaker = sessionmaker(bind=self.engine)
        # If you changed models
        # BaseUsers.metadata.drop_all(self.engine)
        BaseUsers.metadata.create_all(self.engine)

    @contextmanager
    def connect(self):
        session = self.sessionmaker()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def add_user(self, username: str, password: str, token: str = config.DEVICE_TOKEN):
        with self.connect() as session:
            user_meta = UserMeta(name=username, password=password, token=token)
            session.add(user_meta)
            result_id = user_meta.id
        return result_id

    def get_usermeta_by_id(self, user_id: int):
        with self.connect() as session:
            result = session.query(UserMeta).filter(UserMeta.id == user_id).first()
            return result

    def check_user_data(self, username: str, password: str):
        with self.connect() as session:
            result = session.query(UserMeta).filter(UserMeta.name == username,
                                                    UserMeta.password == password).first()
            result_id = result.id if result is not None else None
        return result_id

    def add_task(self, user_id: int, name: str, duration: float, description: str = ''):
        with self.connect() as session:
            task_meta = TaskMeta(name=name, description=description, author_id=user_id,
                                 duration=duration)
            session.add(task_meta)
            result = task_meta.id
        return result

    def remove_task(self, task_id: int):
        with self.connect() as session:
            session.query(TaskMeta).filter(TaskMeta.id == task_id).delete()
            session.query(TaskUserMeta).filter(TaskUserMeta.task_id == task_id).delete()

    def get_tasks(self, user_id: int = None):
        with self.connect() as session:
            if user_id is not None:
                result = session.query(TaskMeta).filter(TaskMeta.author_id == user_id).all()
            else:
                result = session.query(TaskMeta).all()
            return result

    def add_task_executor(self, task_id: int, user_id: int):
        with self.connect() as session:
            if session.query(TaskUserMeta).filter(TaskUserMeta.task_id == task_id,
                                                  TaskUserMeta.user_id == user_id).first() is None:
                session.add(TaskUserMeta(task_id=task_id, user_id=user_id, start_time=datetime.utcnow()))

    def remove_task_executor(self, task_id: int, user_id: int):
        with self.connect() as session:
            task = session.query(TaskMeta).filter(TaskMeta.id == task_id)
            user = self.get_usermeta_by_id(user_id)
            task_user = (session.query(TaskUserMeta)
                                .filter(TaskUserMeta.task_id == task_id, TaskUserMeta.user_id == user_id)
                                .first())

            measures = API.get_involve_estimate(user.token, task_user.start_time,
                                                task_user.start_time + task.duration)

            task_user.results = str(measures)
            session.commit()
