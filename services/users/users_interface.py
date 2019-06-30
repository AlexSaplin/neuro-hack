import json
import numpy
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.config import config
from services.users.models import BaseUsers, UserMeta, TaskMeta, TaskUserMeta
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

    def user_meta_to_dict(self, model: UserMeta):
        return {
            'id': model.id,
            'name': model.name,
            'password': model.password,
            'token': model.token
        } if model is not None else None

    def task_meta_to_dict(self, model: TaskMeta):
        return {
            'id': model.id,
            'name': model.name,
            'description': model.description,
            'author_id': model.author_id,
            'duration': model.duration
        } if model is not None else None

    def add_user(self, username: str, password: str, token: str = config.DEVICE_TOKEN):
        with self.connect() as session:
            user_meta = UserMeta(name=username, password=password, token=token)
            session.add(user_meta)
            result_id = user_meta.id
        return result_id

    def get_usermeta_by_id(self, user_id: int):
        with self.connect() as session:
            result = session.query(UserMeta).filter(UserMeta.id == user_id).first()
            result_dict = self.user_meta_to_dict(result)
        return result_dict

    def check_user_data(self, username: str, password: str):
        with self.connect() as session:
            result = session.query(UserMeta).filter(UserMeta.name == username,
                                                    UserMeta.password == password).first()
            result_id = result.id if result is not None else None
        return result_id

    def add_task(self, user_id: int, name: str, duration: int, description: str = ''):
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
                result_metas = session.query(TaskMeta).filter(TaskMeta.author_id == user_id).all()
            else:
                result_metas = session.query(TaskMeta).all()
            result = list(map(lambda x: self.task_meta_to_dict(x), result_metas))
        return result

    def add_task_executor(self, task_id: int, user_id: int):
        with self.connect() as session:
            if session.query(TaskUserMeta).filter(TaskUserMeta.task_id == task_id,
                                                  TaskUserMeta.user_id == user_id).first() is None:
                session.add(TaskUserMeta(task_id=task_id, user_id=user_id, start_time=datetime.utcnow()))

    def remove_task_executor(self, task_id: int, user_id: int):
        with self.connect() as session:
            task = session.query(TaskMeta).filter(TaskMeta.id == task_id).first()
            user = self.get_usermeta_by_id(user_id)
            task_user = session.query(TaskUserMeta).filter(TaskUserMeta.task_id == task_id,
                                                           TaskUserMeta.user_id == user_id).first()

            measures = API.get_involve_estimate(user.token, task_user.start_time,
                                                task_user.start_time + task.duration)

            task_user.results = str(measures)
            session.commit()

    def fetch_task_results(self, task_id: int):
        with self.connect() as session:
            tasks = session.query(TaskUserMeta).filter(TaskUserMeta.task_id == task_id).all()
            tasks_results = list(map(lambda x: x.results, filter(lambda x: x.results is not None, tasks)))
        if len(tasks_results) == 0:
            return []
        result = []
        for sec_idx in range(len(tasks_results[0])):
            result.append(0.)
            for user_result in tasks_results:
                result[-1] += user_result[sec_idx]
            result[-1] /= len(tasks_results)
        return result
