import uuid

from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from notification.models import UserModel
from notification.database_definition import UserTable
from notification.exceptions import UserAlreadyExists, UserDoesNotExist


class NotificationRepository():
    ENGINE = create_engine("sqlite:///notification/notification.db")

    def __init__(self) -> None:
        self._connection = self.ENGINE.connect()

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
            raise UserDoesNotExist()
        finally:
            self._connection.close()
        return UserModel.model_validate(user)

