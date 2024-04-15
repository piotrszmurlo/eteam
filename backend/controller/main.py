from fastapi import APIRouter

router = APIRouter()


@router.get("/eteam/{service_id}")
def access_service(service_id: int):
    return {'message': 'Eteam app'}
