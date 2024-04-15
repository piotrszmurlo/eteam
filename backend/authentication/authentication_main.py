from fastapi import FastAPI

auth_app = FastAPI()


@auth_app.get("/")
async def root():
    return {"message": "hello auth"}
