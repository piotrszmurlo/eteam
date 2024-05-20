import oci
import uuid
import json

BUCKET_NAME = "bucket-ERSMS"

class FileManager():
    def __init__(self, user_id: uuid.UUID) -> None:
        self.user_data_path = str(user_id)
        config = oci.config.from_file()
        self.object_storage_client = oci.object_storage.ObjectStorageClient(config)
        self.namespace = self.object_storage_client.get_namespace().data

    def insert_file(self, file_id: uuid.UUID, data) -> bool:
        file_path = self.user_data_path + '/'+ str(file_id)
        self.object_storage_client.put_object(self.namespace,BUCKET_NAME,file_path,data)
        return True

    def retrive_file(self, file_id: uuid.UUID):
        file_path = self.user_data_path + '/'+ str(file_id)
        data = self.object_storage_client.get_object(self.namespace,BUCKET_NAME,file_path)
        return bytes(data.data.content)
    
    def delete_file(self, file_id: uuid.UUID) -> None:
        file_path = self.user_data_path + '/'+ str(file_id)
        self.object_storage_client.delete_object(self.namespace,BUCKET_NAME,file_path)
    
    def get_path_to_file(self, file_id: uuid.UUID):
        return self.user_data_path + '/'+ str(file_id)
