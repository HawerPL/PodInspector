### Grafana stack
Mimir, Loki and Tempo for cluster monitoring and PodInspector app.

```
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install lgtm-distributed grafana/lgtm-distributed --version 2.1.0 -f values.yaml
```