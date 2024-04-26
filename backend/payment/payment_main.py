from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from common.dependencies import verify_token



payment_app = FastAPI()


@payment_app.get("/hello")
async def root():
    return {"message": "hello payment"}


