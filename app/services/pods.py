from app.services.kube_client import get_core_v1_api


def get_running_pods():
    core_v1 = get_core_v1_api()
    pods = core_v1.list_pod_for_all_namespaces(watch=False)
    result = []
    for pod in pods.items:
        if pod.status.phase == "Running":
            result.append(
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "node": pod.spec.node_name,
                }
            )
    return result


def get_images():
    return ["nginx:1.23", "redis:7"]


def get_restart_info():
    return [{"name": "app-1", "restarts": 2}]
