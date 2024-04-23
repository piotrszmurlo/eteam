from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey

engine = create_engine("sqlite:///storage/storage.db")

metadata_obj = MetaData()

UserTable = Table(
    "users",
    metadata_obj,
    Column("user_id", String(), primary_key=True),
    Column("user_name", String(), nullable=False),
)

FileTable = Table(
    "files",
    metadata_obj,
    Column("file_id", String(), primary_key=True),
    Column("user_id", String(), ForeignKey("users.user_id"), nullable=False),
    Column("file_name", String(), nullable=False),
)

metadata_obj.create_all(engine)
