from fastapi import FastAPI

from storage import storage_main

app = FastAPI()
app.mount("/backend", storage_main.storage_app)


@app.get("/hello")
async def say_hello():
    return {"message": f"Hello main"}
