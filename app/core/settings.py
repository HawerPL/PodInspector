from pydantic.v1 import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "PodInspector")
    kube_config_file: str = os.getenv("KUBECONFIG", "~/.kube/config")
    enable_profiling: bool = os.getenv("ENABLE_PROFILING", False)
    profiling_endpoint: str = os.getenv("PROFILING_ENDPOINT", "http://k8s-monitoring-alloy-receiver:12345")
    profiling_basic_auth_enabled: bool = os.getenv("PROFILING_BASIC_AUTH_ENABLED", False)
    profiling_basic_auth_username: str = os.getenv("PROFILING_BASIC_AUTH_USERNAME", "admin")
    profiling_basic_auth_password: str = os.getenv("PROFILING_BASIC_AUTH_PASSWORD", "admin")
    enable_tracing: bool = os.getenv("ENABLE_TRACING", False)
    tracing_endpoint: str = os.getenv("TRACING_ENDPOINT", "http://k8s-monitoring-alloy-receiver:12345")

    enable_error_mode_log: bool = os.getenv("ENABLE_ERROR_MODE_LOG", False)
    enable_error_mode_exception: bool = os.getenv("ENABLE_ERROR_MODE_EXCEPTION", False)
    enable_error_mode_soft_crash: bool = os.getenv("ENABLE_ERROR_MODE_SOFT_CRASH", False)
    enable_error_mode_hard_crash: bool = os.getenv("ENABLE_ERROR_MODE_HARD_CRASH", False)
    enable_error_mode_sigkill: bool = os.getenv("ENABLE_ERROR_MODE_SIGKILL", False)
    failure_delay_max_minutes: bool = os.getenv("FAILURE_DELAY_MAX_MINUTES", 3600)

settings = Settings()