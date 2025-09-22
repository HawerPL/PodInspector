### Grafana stack
Pyroscope for cluster monitoring and PodInspector app.

```
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install pyroscope grafana/pyroscope --version 1.15.0 -f values.yaml
```