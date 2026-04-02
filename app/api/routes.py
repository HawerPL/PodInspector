from fastapi import APIRouter, Query
from typing import Annotated

from app.services import pods
from app.services import services

router = APIRouter()

NamespaceQuery = Annotated[str | None, Query(description="Filter by namespace")]


@router.get("/pods")
def get_pods(namespace: NamespaceQuery = None):
    return pods.get_running_pods(namespace=namespace)


@router.get("/services")
def get_services(namespace: NamespaceQuery = None):
    return services.get_services(namespace=namespace)
