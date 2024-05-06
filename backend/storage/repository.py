import uuid

from sqlalchemy import create_engine, select, insert, update, delete, func
from sqlalchemy.exc import IntegrityError

from storage.models import UserModel, FileModel, FileRenameModel, PlanEnum
from storage.database_definition import UserTable, FileTable
from storage.exceptions import (
    UserAlreadyExists,
    UserDoesNotExist,
    FileDoesNotExist,
    StorageLimitExceeded,
)


storage_plans = [
    ["basic", 10, 0],
    ["silver", 50, 50],
    ["gold", 100, 100],
    ["unlimited", float("inf"), 200],
]


class StorageRepository:
    ENGINE = create_engine("sqlite:///storage/storage.db")

    def __init__(self) -> None:
        self._connection = self.ENGINE.connect()

    def insert_user(self, user: UserModel) -> str:
        stmt = insert(UserTable).values(user.model_dump())
        try:
            self._connection.execute(stmt)
            self._connection.commit()
        except IntegrityError:
            raise UserAlreadyExists()
        finally:
            self._connection.close()
        return user.user_id

    def get_user(self, user_id: str) -> UserModel:
        stmt = select(UserTable).where(UserTable.c.user_id == user_id)
        try:
            user = self._connection.execute(stmt).fetchone()
        except IntegrityError:
            raise UserDoesNotExist()
        finally:
            self._connection.close()
        return UserModel.model_validate(user)

    def insert_file(self, file: FileModel) -> uuid.UUID:
        user_query = select(UserTable.c.user_plan).where(
            UserTable.c.user_id == file.user_id
        )
        user_result = self._connection.execute(user_query).first()
        if user_result is None:
            raise UserDoesNotExist("The user does not exist")

        total_files_size_query = select(func.sum(FileTable.c.file_size)).where(
            FileTable.c.user_id == file.user_id
        )
        total_files_size_result = (
            self._connection.execute(total_files_size_query).scalar() or 0
        )
        new_total_size = total_files_size_result + file.file_size
        user_plan_level = user_result.user_plan
        user_plan_limit = storage_plans[user_plan_level][1]
        required_space = new_total_size - user_plan_limit
        if new_total_size > user_plan_limit:
            raise StorageLimitExceeded(
                "Adding this file would exceed the user's storage limit",
                current_plan_level=user_plan_level,
                required_space=required_space,
            )

        insert_stmt = insert(FileTable).values(
            file.model_dump() | {"file_id": str(file.file_id)}
        )
        self._connection.execute(insert_stmt)
        self._connection.commit()
        self._connection.close()

        return file.file_id

    def get_files(self, user_id: str) -> list[FileModel]:
        user_stmt = select(UserTable).where(UserTable.c.user_id == user_id)
        user_result = self._connection.execute(user_stmt).first()
        if user_result is None:
            raise UserDoesNotExist()

        stmt = select(FileTable).where(FileTable.c.user_id == user_id)
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
        if result.rowcount == 0:
            raise FileDoesNotExist()
        self._connection.close()
        return file_id

    def delete_file(self, file_id: uuid.UUID) -> uuid.UUID:
        stmt = delete(FileTable).where(FileTable.c.file_id == str(file_id))
        result = self._connection.execute(stmt)
        self._connection.commit()
        if result.rowcount == 0:
            raise FileDoesNotExist()
        self._connection.close()
        return file_id

    def update_plan(self, user_id: str, plan_level: PlanEnum):
        update_dict = {"user_plan": plan_level}

        stmt = (
            update(UserTable).where(UserTable.c.user_id == user_id).values(update_dict)
        )

        result = self._connection.execute(stmt)
        self._connection.commit()

        return {f"Plan updated for user: {user_id}"}
