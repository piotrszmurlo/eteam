import uuid
from pathlib import Path, PurePath
import os
from storage.exceptions import FileDoesNotExist

STORAGE_FS_PATH = PurePath(os.path.dirname(__file__), 'storage_fs')


class FileManager():
    """ Baisc file system tree responsible for storing user data:

            |storage_fs
                |user's folder, name: <some_user_id>
                    |user's file, name: <some_file_id>
                    ...
                ...
    """
    def __init__(self) -> None:
        pass

    def insert_file(self, user_id: uuid.UUID, file_id: uuid.UUID, data) -> bool:
        file_path = Path(STORAGE_FS_PATH, str(user_id), str(file_id))
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, 'w+') as user_file:
                user_file.write(data)
        except IOError:
            return False
        return True

    def retrive_file(self, user_id: uuid.UUID, file_id: uuid.UUID):
        file_path = Path(STORAGE_FS_PATH, str(user_id), str(file_id))
        if file_path.exists():
            return file_path.read_text() # or read_bytes()
        
        else:
            raise FileDoesNotExist
