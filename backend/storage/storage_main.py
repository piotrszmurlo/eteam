from fastapi import FastAPI

storage_app = FastAPI()


@storage_app.get("/hello")
async def root():
    return {"message": "hello storage"}
