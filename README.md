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

| Environment                      | Description                                                                       | Default value                              |
|----------------------------------|-----------------------------------------------------------------------------------|--------------------------------------------|
| KUBECONFIG                         | Lokalizacja pliku konfiguracji klienta k8s dla aplikacji wdrożonej poza klastrem. | ~/.kube/config                             |
| APP_NAME                         | Nazwa aplikacji.                                                                  | PodInspector                               |
| ENABLE_PROFILING                         | Uruchomienie profilowania.                                                        | ~/.kube/config                             |
| PROFILING_ENDPOINT                         | Adres końcowy profilowania.                                                       | http://k8s-monitoring-alloy-receiver:12345 |
| PROFILING_BASIC_AUTH_ENABLED                         | Włączenie autoryzacji dla profilowania.                                           | False                             |
| PROFILING_BASIC_AUTH_USERNAME                         | Nazwa użytkownika dla autoryzowanego profilowania.                                | admin                            |
| PROFILING_BASIC_AUTH_PASSWORD                         | Hasło użytkownika dla autoryzowanego profilowania.                                | admin                           |
| ENABLE_TRACING                         | Uruchomienie tracingu.                                                            | False                                      |
| TRACING_ENDPOINT                         | Adres końcowy tracingu.                                                           | http://k8s-monitoring-alloy-receiver:12345 |
| ENABLE_ERROR_MODE_LOG                         | Uruchomienie trybu awarii - log.                                                  | False                                      |
| ENABLE_ERROR_MODE_EXCEPTION                         | Uruchomienie trybu awarii - wyjątek.                                              | False                                      |
| ENABLE_ERROR_MODE_SOFT_CRASH                         | Uruchomienie trybu awarii soft crash.                                             | False                                      |
| ENABLE_ERROR_MODE_HARD_CRASH                         | Uruchomienie trybu awarii - hard crash.                                           | False                                      |
| ENABLE_ERROR_MODE_SIGKILL                         | LUruchomienie trybu awarii - SIGKILL.                                             | False                                      |
| FAILURE_DELAY_MAX_MINUTES                         | .                                                                                 | 3600                                       |

## Uruchomienie aplikacji

### Docker
W celu uruchomienia aplikacji poza klastrem w dockerze należy przekazać lokalizację pliku konfiguracyjnego klienta k8s.
```
docker run -p 8080:8080 -v /home/hawer/podinspector/KUBECONFIG:/tmp/KUBECONFIG -e KUBECONFIG=/tmp/KUBECONFIG podinspector:latest
```

### Helm


```
helm update --install monitoring charts/PodInspector -f charts/PodInspector/values.yaml
```