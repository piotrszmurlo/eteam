from fastapi import FastAPI

notification_app = FastAPI()


@notification_app.get("/hello")
async def root():
    return {"message": "hello notification"}
