# 2 — Distributed Tracing
## Using HoneyComb
* Configure our instrumentation variables in Dockerfile
* OTEL is an OpenTelemetry source code popularilu used
```
OTEL_SERVICE_NAME: "backend-flask"
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
```
* We also need to install the python modules required. Can insert in our *requirements.txt*
```
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```