---
tags:
  - OpenTelemetry
  - SRE
---

# Collector

> *Vendor-agnostic way to receive, process and export telemetry data.* - [Collector | OpenTelemetry Docs](https://opentelemetry.io/docs/collector/)

![](https://opentelemetry.io/docs/collector/img/otel-collector.svg)
/// caption
[OpenTelemetry Collector Architecture](https://opentelemetry.io/docs/collector/)
///

- In general we recommend using a collector alongside your service, since it allows your service to offload data quickly and the collector can take care of additional handling