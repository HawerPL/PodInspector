from fastapi import APIRouter

from app.services import pods

router = APIRouter()

@router.get("/pods")
def get_pods():
    return pods.get_running_pods()