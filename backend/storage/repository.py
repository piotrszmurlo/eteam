import uuid

from sqlalchemy import create_engine, select, insert, update, delete

from storage.models import UserModel, FileModel
from storage.database_definition import UserTable, FileTable


class StorageRepository():
    def __init__(self) -> None:
        engine = create_engine("sqlite:///storage/storage.db")
        self._connection = engine.connect()

    def insert_user(self, user: UserModel) -> str:
        stmt = (
            insert(UserTable).values(user.model_dump())
        )
        self._connection.execute(stmt)
        self._connection.commit()
        self._connection.close()
        return user.user_id

    def get_user(self, user_id: str) -> UserModel:
        stmt = (
            select(UserTable).where(UserTable.c.user_id == user_id)
        )
        user = self._connection.execute(stmt).fetchone()
        self._connection.close()
        return UserModel.model_validate(user)

    def insert_file(self, file: FileModel) -> uuid.UUID:
        stmt = (
            insert(FileTable).values(file.model_dump() | {"file_id": str(file.file_id)})
        )
        self._connection.execute(stmt)
        self._connection.commit()
        self._connection.close()
        return file.file_id

    def get_files(self, user_id: str) -> list[FileModel]:
        stmt = (
            select(FileTable).where(FileTable.c.user_id == user_id)
        )
        files = self._connection.execute(stmt).fetchall()
        self._connection.close()
        return [FileModel.model_validate(file) for file in files]

    def rename_file(self, file_id: uuid.UUID, new_file_name: str) -> uuid.UUID:
        stmt = (
            update(FileTable)
            .where(FileTable.c.file_id == str(file_id))
            .values(file_name=new_file_name)
        )
        self._connection.execute(stmt)
        self._connection.commit()
        self._connection.close()
        return file_id
    
    def delete_file(self, file_id: uuid.UUID) -> uuid.UUID:
        stmt = (
                delete(FileTable)
                .where(FileTable.c.file_id == str(file_id))
        )
        self._connection.execute(stmt)
        self._connection.commit()
        self._connection.close()
        return file_id