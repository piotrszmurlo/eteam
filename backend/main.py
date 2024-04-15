from fastapi import FastAPI

from storage import storage_main
from authentication import authentication_main

app = FastAPI()
app.mount("/storage", storage_main.storage_app)
app.mount("/auth", authentication_main.auth_app)


@app.get("/hello")
async def say_hello():
    return {"message": f"Hello main"}
