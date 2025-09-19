import logging
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

from app.core.settings import settings

logger = logging.getLogger(__name__)
_core_v1 = None


def init_kube_client():
    logging.info(f"KUBECONFIG={settings.kube_config_file}")
    global _core_v1
    try:
        config.load_kube_config(config_file=settings.kube_config_file)
        logger.info("Loaded kube config from ~/.kube/config")
    except ConfigException:
        config.load_incluster_config()
        logger.info("Loaded in-cluster kubpip e config")
    _core_v1 = client.CoreV1Api()


def get_core_v1_api():
    if _core_v1 is None:
        raise RuntimeError(
            "Kubernetes client not initialized. Call init_kube_client() first."
        )
    return _core_v1
