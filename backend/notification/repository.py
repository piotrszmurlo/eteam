import uuid

from sqlalchemy import create_engine, select, insert, update, delete

from notification.models import UserModel
from notification.database_definition import UserTable


class NotificationRepository():
    def __init__(self) -> None:
        engine = create_engine("sqlite:///notification/notification.db")
        self._connection = engine.connect()

    def insert_user(self, user: UserModel) -> str:
        stmt = (
            insert(UserTable).values(user.model_dump())
        )
    
        self._connection.execute(stmt)
        self._connection.commit()
        self._connection.close()

        return user.user_id
