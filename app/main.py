from fastapi import FastAPI

from app.api.routes import router
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.logging_config import init_logging
from app.core.settings import settings
from app.services.failure_simulator import simulate_failure
from app.services.kube_client import init_kube_client


init_logging()

if settings.enable_profiling:
    import pyroscope

    pyroscope.configure(
        application_name=settings.app_name,
        server_address=settings.profiling_address,
        sample_rate=100,
    )
app = FastAPI(title=settings.app_name, version="1.0", log_config=None)
Instrumentator().instrument(app).expose(app)

app.include_router(router)


# TODO: Zaktualizować do lifespan
@app.on_event("startup")
def startup_event():
    init_kube_client()
    if (
        settings.enable_error_mode_log
        or settings.enable_error_mode_exception
        or settings.enable_error_mode_soft_crash
        or settings.enable_error_mode_hard_crash
        or settings.enable_error_mode_sigkill
    ):
        simulate_failure()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    # tutaj możesz dodać np. sprawdzenie Redis/K8s
    return {"status": "ready"}
