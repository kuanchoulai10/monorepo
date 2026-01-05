---
tags:
  - Flagger
  - Progressive Delivery
  - How It Works
---

# How Flagger Works? - Istio Integration

In this document, we will explore how Flagger integrates with Istio to enable progressive delivery.

## Core Concepts

![](https://docs.flagger.app/~gitbook/image?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffluxcd%2Fflagger%2Fmain%2Fdocs%2Fdiagrams%2Fflagger-overview.png&width=768&dpr=2&quality=100&sign=87fa55d&sv=2)
/// caption
Flagger overview diagram
///

Flagger is a **progressive delivery** tool that automates the release process for applications running on Kubernetes. It works by **monitoring application metrics** and **gradually shifting traffic to new versions based on predefined rules and analysis**.

It supports multiple **routing providers**, all with different levels of integration and features. Some of the supported routing providers include:

- **Istio**
- Linkerd
- App Mesh
- NGINX
- Skipper
- Contour
- Gloo Edge
- Traefik
- Kuma
- Gateway API
- Apache APISIX
- Knative

In this document, we will focus on how Flagger works with **Istio** since **it supports a wide range of deployment strategies and advanced traffic management features**. See [Deployment Strategies](https://docs.flagger.app/main/usage/deployment-strategies) for more details.

### Deployment Strategies
 
Flagger supports various **deployment strategies**, including:

- **Canary Release**: Gradually shifts traffic from the stable version to the new version in incremental steps based on predefined rules and metric analysis
- **A/B Testing**: Routes traffic to different versions based on HTTP headers or cookies to compare performance and user behavior
- **Blue/Green**: Switches traffic instantly from the old version (blue) to the new version (green) after validation
- **Blue/Green Mirroring**: Mirrors production traffic to the new version for testing without affecting user requests, then switches when ready
- **Canary Release with Session Affinity**: Gradually shifts traffic to the new version while maintaining user sessions on the same version using cookie-based routing

![](https://docs.flagger.app/~gitbook/image?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffluxcd%2Fflagger%2Fmain%2Fdocs%2Fdiagrams%2Fflagger-canary-steps.png&width=768&dpr=4&quality=100&sign=de1f0364&sv=2)
/// caption
[Flagger Canary Stages](https://docs.flagger.app/main/usage/deployment-strategies#canary-release)
///

![](https://docs.flagger.app/~gitbook/image?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffluxcd%2Fflagger%2Fmain%2Fdocs%2Fdiagrams%2Fflagger-abtest-steps.png&width=768&dpr=4&quality=100&sign=45ebadf7&sv=2)
/// caption
[Flagger A/B Testing Stages](https://docs.flagger.app/main/usage/deployment-strategies#a-b-testing)
///

![](https://docs.flagger.app/~gitbook/image?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffluxcd%2Fflagger%2Fmain%2Fdocs%2Fdiagrams%2Fflagger-bluegreen-steps.png&width=768&dpr=4&quality=100&sign=ad9af801&sv=2)
/// caption
[Flagger Blue/Green Stages](https://docs.flagger.app/main/usage/deployment-strategies#blue-green-deployments)
///

See [Deployment Strategies](https://docs.flagger.app/main/usage/deployment-strategies) for more details.


### Metrics Analysis

During the deployment process, Flagger can **continuously monitor the metrics we care about**, such as error rate percentage, availability, or average response time. Common metric sources include [Prometheus](https://docs.flagger.app/main/usage/metrics#prometheus), [CloudWatch](https://docs.flagger.app/main/usage/metrics#amazon-cloudwatch), Datadog, New Relic, and others. See [Metrics Analysis](https://docs.flagger.app/main/usage/metrics) for more details.

### Alerting

Flagger supports sending alerts to various channels, including **Slack**, **Microsoft Teams**, **Rocket.Chat**, and **Discord**.

At the global level, Slack and Microsoft Teams can be configured.

At the per `Canary` level, Slack, Microsoft Teams, Rocket.Chat and Discord can be configured. The canary analysis can be extended with a list of alerts that reference an `AlertProvider`.

See [Alerting](https://docs.flagger.app/main/usage/alerting) for more details.

### CRDs

- **`Canary`**: The Canary custom resource defines the deployment strategy, analysis metrics, and traffic routing rules for a specific application.
- **`MetricTemplate`**: This resource allows users to define custom metrics for analysis during the deployment process.
- **`AlertProvider`**: This resource configures alerting channels for deployment notifications.

### Istio Integration

Flagger uses Istio's traffic management capabilities to perform **canary deployments**, **A/B testing**, **traffic mirroring**, and **blue/green deployments**. It leverages Istio's `VirtualServices` and `DestinationRules` to control the flow of traffic between different versions of an application. 

![](https://docs.flagger.app/~gitbook/image?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffluxcd%2Fflagger%2Fmain%2Fdocs%2Fdiagrams%2Fflagger-canary-hpa.png&width=768&dpr=4&quality=100&sign=f510931c&sv=2)
/// caption
[Flagger Canary Process](https://docs.flagger.app/main/tutorials/istio-progressive-delivery)
///

## Behind the Scenes

