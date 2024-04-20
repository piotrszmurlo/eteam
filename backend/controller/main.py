from fastapi import APIRouter

from fastapi import APIRouter, HTTPException, Request, Query
from starlette.responses import RedirectResponse

router = APIRouter()


# @router.get("/{service_id}")
# def access_service(service_id: int):
#     return {'message': 'Eteam app'}

@router.get("/{service_id}")
def access_service(service_id: int, token: dict):
    # user_name = token["name"]
    print(token)
    return {'message': f'Eteam app'}

