# PodInspector
Prosta aplikacja stworzona do nauki tworzenia helm chartów, korzystania z ArgoCD oraz konfiguracji monitoringów w Grafanie.

## Spis treści
* [Budowanie obrazu aplikacji](#budowanie-obrazu-aplikacji)
* [Konfiguracja](#konfiguracja)
* [Uruchomienie aplikacji](#uruchomienie-aplikacji)

## Budowanie obrazu aplikacji

```
docker build -t podinspector:latest
```

## Konfiguracja

---

| Environment                      | Description                                                                       | Default value      |
|----------------------------------|-----------------------------------------------------------------------------------|--------------------|
| KUBECONFIG                         | Lokalizacja pliku konfiguracji klienta k8s dla aplikacji wdrożonej poza klastrem. | ~/.kube/config |

## Uruchomienie aplikacji

### Docker
W celu uruchomienia aplikacji poza klastrem w dockerze należy przekazać lokalizację pliku konfiguracyjnego klienta k8s.
```
docker run -p 8080:8080 -v /home/hawer/podinspector/KUBECONFIG:/tmp/KUBECONFIG -e KUBECONFIG=/tmp/KUBECONFIG podinspector:latest
```

### Helm