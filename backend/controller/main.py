from fastapi import APIRouter

router = APIRouter()


@router.post("/{service_id}")
def access_service_post(service_id: str):
    return {'message': 'Eteam app'}


@router.get("/{service_id}")
def access_service(service_id: str):
    return {'message': 'Eteam app'}
