from fastapi import FastAPI

from storage import storage_main

app = FastAPI()
app.mount("/backend/storage", storage_main.storage_app)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
