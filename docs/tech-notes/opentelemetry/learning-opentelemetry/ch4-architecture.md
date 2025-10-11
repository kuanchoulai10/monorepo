---
tags:
  - OpenTelemetry
  - SRE
---

# Ch4 Architecture

--8<-- "./docs/disclaimer.md"

OpenTelemetry consists of three kinds of components: 

- instrumentation installed within applications,
- exporters for infrastructure such as Kubernetes, and
- pipeline components for sending all of this telemetry to a storage system.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098147174/files/assets/leot_0401.png)
/// caption
The relationship between OpenTelemetry and analysis components
///

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098147174/files/assets/leot_0402.png)
/// caption
OpenTelemetry application architecture
///


!!! info "Application Telemetry"

    - Library Instrumentation
    - **The OpenTelemetry API**: it's safe to call even when OpenTelemetry is not installed within an application.
    - **The OpenTelemetry SDK**: a plug-in framework consisting of sampling algorithms, lifecycle hooks, and exporters

!!! info "Infrastructure Telemetry"

    OpenTelemetry is slowly being added to Kubernetes and other cloud services. OpenTelemetry comes with a number of components that can be used to gather infrastructure services' telemetry and add it into the pipeline of telemetry coming from applications.



Telemetry Pipelines

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098147174/files/assets/leot_0412.png)
/// caption
The new model of observability tools
///
