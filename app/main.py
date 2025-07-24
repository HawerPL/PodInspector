from fastapi import FastAPI

from app.api.routes import router
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.logging_config import init_logging
from app.services.kube_client import init_kube_client



init_logging()
app = FastAPI(title="PodInspector", version="1.0")
Instrumentator().instrument(app).expose(app)

app.include_router(router)


#TODO: Zaktualizować do lifespan
@app.on_event("startup")
def startup_event():
    init_kube_client()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    # tutaj możesz dodać np. sprawdzenie Redis/K8s
    return {"status": "ready"}