from fastapi import FastAPI

storage_app = FastAPI()


@storage_app.get("/")
async def root():
    return {"message": "storage World"}
