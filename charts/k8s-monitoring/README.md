### K8s-monitoring for Grafana stack
Alloy integration for PodInspector app with cluster monitoring

```
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install k8s-monitoring grafana/k8s-monitoring -n monitoring --version 3.1.0 -f values.yaml
```