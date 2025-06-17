from pydantic.v1 import BaseSettings
import os

class Settings(BaseSettings):
    kube_config_file: str = os.getenv("KUBECONFIG", "~/.kube/config")

settings = Settings()