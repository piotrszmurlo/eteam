import uuid

from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from notification.models import UserModel
from notification.database_definition import UserTable

from notification.exceptions import UserAlreadyExists, UserDoesNotExists


class NotificationRepository():
    def __init__(self) -> None:
        engine = create_engine("sqlite:///notification/notification.db")
        self._connection = engine.connect()

    def insert_user(self, user: UserModel) -> str:
        stmt = (
            insert(UserTable).values(user.model_dump())
        )
    
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise UserAlreadyExists()
        finally:
            self._connection.close()
        return user.user_id
    
    def get_user(self, user_id: str) -> UserModel:
        stmt = (
            select(UserTable).where(UserTable.c.user_id == user_id)
        )
        try:
            user = self._connection.execute(stmt).fetchone()
        except IntegrityError:
            raise UserDoesNotExists()
        finally:
            self._connection.close()
        return UserModel.model_validate(user)
