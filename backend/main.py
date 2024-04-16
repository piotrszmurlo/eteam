from uuid import uuid4

from fastapi import FastAPI, Depends, Request, Response
from starlette.responses import RedirectResponse, JSONResponse

from gateway.api_router import call_api_gateway, RedirectStorageServiceException, RedirectNotificationPortalException, \
    RedirectLibraryPortalException
from storage import storage_main
from authentication import authentication_main
from notification import notification_main
from controller import main
from loguru import logger

app = FastAPI()
app.include_router(main.router, dependencies=[Depends(call_api_gateway)])

app.mount("/storage", storage_main.storage_app)
app.mount("/auth", authentication_main.auth_app)
app.mount("/notification", notification_main.notification_app)
logger.add("info.log", format="Log: [{extra[log_id]}: {time} - {level} - {message} ", level="INFO", enqueue=True)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        logger.info('Request to access ' + request.url.path)
        try:
            response = await call_next(request)
        except Exception as ex:
            logger.error(f"Request to " + request.url.path + " failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        finally:
            logger.info('Successfully accessed ' + request.url.path)
            return response


@app.exception_handler(RedirectStorageServiceException)
def exception_handler_student(request: Request, exc: RedirectStorageServiceException) -> Response:
    return RedirectResponse(url='http://localhost:8000/storage/hello')


@app.exception_handler(RedirectNotificationPortalException)
def exception_handler_faculty(request: Request, exc: RedirectNotificationPortalException) -> Response:
    return RedirectResponse(url='http://localhost:8000/notification/hello')


@app.exception_handler(RedirectLibraryPortalException)
def exception_handler_library(request: Request, exc: RedirectLibraryPortalException) -> Response:
    return RedirectResponse(url='http://localhost:8000/library/hello')


@app.get("/hello")
async def say_hello():
    return {"message": f"Hello main"}
