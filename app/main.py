from fastapi import FastAPI

from app.api.routes import router
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.logging_config import init_logging
from app.core.settings import settings
from app.services.failure_simulator import simulate_failure
from app.services.kube_client import init_kube_client
import logging

init_logging()

if settings.ENABLE_PROFILING:
    import pyroscope

    logging.info(f"Enabling Profiling")
    pyroscope.configure(
        application_name=settings.APP_NAME,
        server_address=settings.PROFILING_ENDPOINT,
        sample_rate=100,
        detect_subprocesses=False,
        oncpu=True,
        gil_only=True,
    )
app = FastAPI(title=settings.APP_NAME, version="1.0", log_config=None)
Instrumentator().instrument(app).expose(app)

app.include_router(router)


# TODO: Zaktualizować do lifespan
@app.on_event("startup")
def startup_event():
    init_kube_client()
    if (
        settings.ENABLE_ERROR_MODE_LOG
        or settings.ENABLE_ERROR_MODE_EXCEPTION
        or settings.ENABLE_ERROR_MODE_SOFT_CRASH
        or settings.ENABLE_ERROR_MODE_HARD_CRASH
        or settings.ENABLE_ERROR_MODE_SIGKILL
    ):
        logging.debug(
            f"""
            MODE_LOG: {settings.ENABLE_ERROR_MODE_LOG}
            MODE_EXCEPT: {settings.ENABLE_ERROR_MODE_EXCEPTION}
            MODE_SOFT: {settings.ENABLE_ERROR_MODE_SOFT_CRASH}
            MODE_HARD: {settings.ENABLE_ERROR_MODE_HARD_CRASH}
            MODE_SIGKILL: {settings.ENABLE_ERROR_MODE_SIGKILL}"""
        )
        simulate_failure()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    # tutaj możesz dodać np. sprawdzenie Redis/K8s
    return {"status": "ready"}
