# TODO: Do głębszej analizy jak to działa i jak to wzorcowo używać
{{- define "pod-inspector.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}