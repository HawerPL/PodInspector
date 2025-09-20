from pydantic.v1 import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "PodInspector"
    KUBECONFIG: str = "~/.kube/config"
    ENABLE_PROFILING: bool = True
    PROFILING_ENDPOINT: str = "http://k8s-monitoring-alloy-receiver:12345"
    PROFILING_BASIC_AUTH_ENABLED: bool = False
    PROFILING_BASIC_AUTH_USERNAME: str = "admin"
    PROFILING_BASIC_AUTH_PASSWORD: str = "admin"
    ENABLE_TRACING: bool = False
    TRACING_ENDPOINT: str = "http://k8s-monitoring-alloy-receiver:12345"

    ENABLE_ERROR_MODE_LOG: bool = False
    ENABLE_ERROR_MODE_EXCEPTION: bool = False
    ENABLE_ERROR_MODE_SOFT_CRASH: bool = False
    ENABLE_ERROR_MODE_HARD_CRASH: bool = False
    ENABLE_ERROR_MODE_SIGKILL: bool = False
    FAILURE_DELAY_MAX_MINUTES: int = 3600

    class Config:
        env_file: Optional[str] = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
