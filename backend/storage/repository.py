import uuid

from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from storage.models import UserModel, FileModel, FileRenameModel
from storage.database_definition import UserTable, FileTable
from storage.exceptions import UserAlreadyExists, UserDoesNotExists, FileAlreadyExists, FileDoesNotExists

import logging


class StorageRepository():
    ENGINE = create_engine("sqlite:///storage/storage.db")

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
            raise UserDoesNotExists()
        finally:
            self._connection.close()
        return UserModel.model_validate(user)

    def insert_file(self, file: FileModel) -> uuid.UUID:
        stmt = (
            insert(FileTable).values(file.model_dump() | {"file_id": str(file.file_id)})
        )

        # FIXME: czy tutaj jakiś try/except powinien być?
        self._connection.execute(stmt)
        self._connection.commit()
        self._connection.close()
        return file.file_id

    def get_files(self, user_id: str) -> list[FileModel]:
        # FIXME: to samo co wyżej
        # jak nie ma takiego użytkownika to i tak zwraca []
        user_stmt = select(UserTable).where(UserTable.c.user_id == user_id)
        user_result = self._connection.execute(user_stmt).first()
        if user_result is None:
            raise UserDoesNotExists()

        stmt = (
            select(FileTable).where(FileTable.c.user_id == user_id)
        )
        files = self._connection.execute(stmt).fetchall()
        self._connection.close()
        return [FileModel.model_validate(file) for file in files]

    def rename_file(self, file_id: uuid.UUID, new_file: FileRenameModel) -> uuid.UUID:
        # sprawdzenie czy żądanie jest puste
        update_dict = new_file.model_dump(exclude_none=True)
        if not update_dict:
            return file_id

        stmt = (
            update(FileTable)
            .where(FileTable.c.file_id == str(file_id))
            .values(update_dict)
        )

        result = self._connection.execute(stmt)
        self._connection.commit()
        # sprawdzenie czy update coś zmienił
        # bo nawet jak ID jest błędne to po prostu nic nie zmienia
        if result.rowcount == 0:
            raise FileDoesNotExists()
        self._connection.close()
        return file_id
    
    def delete_file(self, file_id: uuid.UUID) -> uuid.UUID:
        stmt = (
                delete(FileTable)
                .where(FileTable.c.file_id == str(file_id))
        )
        result = self._connection.execute(stmt)
        self._connection.commit()
        # analogiczne sprawdzenie jak wyżej
        if result.rowcount == 0:
            raise FileDoesNotExists()
        self._connection.close()
        return file_id