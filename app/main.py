import platform
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.logging_config import init_logging
from app.core.settings import settings
from app.services.failure_simulator import simulate_failure
from app.services.kube_client import init_kube_client
import logging

init_logging()

if settings.ENABLE_PROFILING and platform.system() != "Windows":
    import pyroscope

    logging.info("Enabling Profiling")
    pyroscope.configure(
        application_name=settings.APP_NAME,
        server_address=settings.PROFILING_ENDPOINT,
        sample_rate=100,
        oncpu=True,
        gil_only=False,
        enable_logging=settings.ENABLE_PROFILING_DEBUG,
        tags={"hostname": platform.node()},
    )

if settings.ENABLE_TRACING:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    otlp_exporter = OTLPSpanExporter(endpoint=settings.TRACING_ENDPOINT, insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    LoggingInstrumentor().instrument(set_logging_format=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application startup")

    init_kube_client()

    if (
        settings.ENABLE_ERROR_MODE_LOG
        or settings.ENABLE_ERROR_MODE_EXCEPTION
        or settings.ENABLE_ERROR_MODE_SOFT_CRASH
        or settings.ENABLE_ERROR_MODE_HARD_CRASH
        or settings.ENABLE_ERROR_MODE_SIGKILL
    ):
        logging.debug(f"""
            MODE_LOG: {settings.ENABLE_ERROR_MODE_LOG}
            MODE_EXCEPT: {settings.ENABLE_ERROR_MODE_EXCEPTION}
            MODE_SOFT: {settings.ENABLE_ERROR_MODE_SOFT_CRASH}
            MODE_HARD: {settings.ENABLE_ERROR_MODE_HARD_CRASH}
            MODE_SIGKILL: {settings.ENABLE_ERROR_MODE_SIGKILL}""")
        simulate_failure()

    yield

    logging.info("Application shutdown")


def create_app():
    app = FastAPI(
        title=settings.APP_NAME, version="1.0", log_config=None, lifespan=lifespan
    )
    app.include_router(router)
    return app


app = create_app()

if settings.ENABLE_TRACING:
    FastAPIInstrumentor.instrument_app(app)

Instrumentator().instrument(app).expose(app)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    return {"status": "ready"}
