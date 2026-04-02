from app.services.kube_client import get_core_v1_api


def get_services(namespace: str | None = None) -> list[dict]:
    core_v1 = get_core_v1_api()

    if namespace:
        raw_services = core_v1.list_namespaced_service(namespace, watch=False)
    else:
        raw_services = core_v1.list_service_for_all_namespaces(watch=False)

    return [
        {"name": service.metadata.name, "namespace": service.metadata.namespace}
        for service in raw_services.items
    ]
