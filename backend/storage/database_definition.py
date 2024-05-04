from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey, Float, Enum, Integer

engine = create_engine("sqlite:///storage/storage.db")

metadata_obj = MetaData()

UserTable = Table(
    "users",
    metadata_obj,
    Column("user_id", String(), primary_key=True),
    Column("user_name", String(128), nullable=False),
    # Column("user_plan", Enum("basic", "silver", "gold", "unlimited"), nullable=False)
    Column("user_plan", String(128), nullable=False)

)

FileTable = Table(
    "files",
    metadata_obj,
    Column("file_id", String(), primary_key=True),
    Column("user_id", String(), ForeignKey("users.user_id"), nullable=False),
    Column("file_name", String(), nullable=False),
    Column("file_size", Float(), nullable=False)
)

metadata_obj.create_all(engine)
