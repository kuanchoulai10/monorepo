---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2026-06-16
  updated: 2026-06-16
categories:
  - Data
links:
  - blog/posts/2026/01-06/what-iceberg-doesnt-solve-for-netflix/what-iceberg-doesnt-solve-for-netflix.md
  - blog/posts/2026/01-06/iceberg-challenges-from-the-field/iceberg-challenges-from-the-field.md
  - blog/posts/2026/01-06/rethinking-iceberg-metadata-v4/rethinking-iceberg-metadata-v4.md
  - blog/posts/2026/01-06/lessons-from-slack-iceberg/lessons-from-slack-iceberg.md
  - blog/posts/2026/01-06/iceberg-efficient-column-update-and-column-families/iceberg-efficient-column-update-and-column-families.md
  - "AutoComp: Automated Data Compaction for Log-Structured Tables in Data Lakes (arXiv, Apr 2025)": https://arxiv.org/abs/2504.04186
  - "Zero-Scan Data Quality: Leveraging Table Format Metadata for Continuous Observability at Scale (arXiv, May 2026)": https://arxiv.org/abs/2605.30308
  - "Optimizing Iceberg Table Layouts at Scale: A Multi-Objective Approach (2025 Iceberg Summit)": https://www.youtube.com/watch?v=Gjmg8aPJeIk
  - "Taking Charge of Tables with OpenHouse (2024 Confluent Current)": https://www.youtube.com/watch?v=5fubVf6E3PM
  - "linkedin/openhouse (GitHub)": https://github.com/linkedin/openhouse
  - "AWS re:Invent 2023 - Netflix's journey to an Apache Iceberg–only data lake (NFX306)": https://www.youtube.com/watch?v=jMFMEk8jFu8
  - "Learnings from Running Large-scale Apache Iceberg™ Table Management Service (2025 Iceberg Summit)": https://www.youtube.com/watch?v=JN6K1pdFImc
  - "Maintaining Iceberg at Scale: Lessons from Slack (2026 Iceberg Summit)": https://www.youtube.com/watch?v=NRSlundcwvc
  - "Floe: Policy-Based Table Maintenance for Apache Iceberg (Berlin Buzzwords)": https://www.youtube.com/watch?v=UN44R8jYSXk
  - "nssalian/floe (GitHub)": https://github.com/nssalian/floe
  - "LakeOps": https://lakeops.dev/
tags:
  - Apache Iceberg
comments: true
---

# Iceberg Table Maintenance at Scale

!!! info "TLDR"

    After reading this article, you will learn:

    - TBD
    - TBD
    - TBD

<!-- more -->

## Slack

![Slack Architecture Diagram](./assets/slack-architecture-diagram.png)
/// caption
[Architecture Diagram](https://www.youtube.com/watch?v=NRSlundcwvc)
///

![Slack Components](./assets/slack-components.png)
/// caption
[Components](https://www.youtube.com/watch?v=NRSlundcwvc)
///


## Netflix

![Netflix Metadata Service](./assets/netflix-metadata-service.png)
/// caption
[Metadata Service](https://www.youtube.com/watch?v=jMFMEk8jFu8)
///

![Netflix Metadata Service Details](./assets/netflix-metadata-service-details.png)
/// caption
[Details of Metadata Service](https://www.youtube.com/watch?v=jMFMEk8jFu8)
///

![Netflix Janitor](./assets/netflix-janitor.png)
/// caption
[Janitor](https://www.youtube.com/watch?v=jMFMEk8jFu8)
///

![Netflix Autotune](./assets/netflix-autotune.png)
/// caption
[Autotune](https://www.youtube.com/watch?v=jMFMEk8jFu8)
///

## Apple

![Apple Architecture](./assets/apple-architecture.png)
/// caption
[Architecture](https://www.youtube.com/watch?v=JN6K1pdFImc)
///

![Apple Spark Job T-Shirt Sizing + Priorities](./assets/apple-spark-job-tshirt-sizing.png)
/// caption
[Spark Job T-Shirt Sizing + Priorities](https://www.youtube.com/watch?v=JN6K1pdFImc)
///

Workload Scaling

Push-based: Difficult to scale

![Apple Push-based](./assets/apple-push-based.png)
/// caption
[Push-based](https://www.youtube.com/watch?v=JN6K1pdFImc)
///

![Apple Pull-based](./assets/apple-pull-based.png)
/// caption
[Pull-based](https://www.youtube.com/watch?v=JN6K1pdFImc)
///
per catalog, per-workload type, per security profile (need to design queue strategy very quickly)

![Apple TMS Enhancements](./assets/apple-tms-enhancements.png)
/// caption
[TMS Enhancements](https://www.youtube.com/watch?v=JN6K1pdFImc)
///

event-based management
- extend iceberg rest spec with events
- TMS runs based on catalog events
    - Ingestion volume threshold
    - Ingestion Count Threshold
    - Small File Count Threshold
    - Table Update / Delete event

## LinkedIn

### AutoComp

!!! 
**Functional Requirements**

- **Fine-grained work units**. AutoComp should automatically select compaction candidates based on dynamic data analysis
- **Support for multiple compaction strategies**. The framework should support various compaction strategies that can encode the benefits, costs, or a combination of both, depending on the optimization objective.
- **Periodic and post-write execution triggers**. The framework should support execution triggered both periodically and immediately after large write operations.

**Non-Functional Requirements**

- **Extensibility**. The framework should be designed with future extensibility in mind, enabling it to integrate additional compaction strategies and adapt to new workloads as needed.
- **Explainability**. The framework should produce consistent compaction decisions under identical input conditions (e.g., file size distribution, workload characteristics).
- **Cross-platform compatibility**. The framework should be designed to work seamlessly across different LST and catalog implementations.

![End-to-end workflow for AutoComp](./assets/linkedin-autocomp-end-to-end-workflow.png)
/// caption
[End-to-end workflow for AutoComp](https://arxiv.org/pdf/2504.04186)
///

![Cluster Integration of AutoComp](./assets/linkedin-autocomp-cluster-integration.png)
/// caption
[Cluster Integration of AutoComp](https://arxiv.org/pdf/2504.04186)
///

### OpenHouse

![](https://github.com/linkedin/openhouse/blob/main/docs/images/openhouse-controlplane.jpeg?raw=true)
/// caption
[OpenHouse](https://github.com/linkedin/openhouse)
///


## Floe

<iframe width="560" height="315" src="https://www.youtube.com/embed/UN44R8jYSXk?si=zq8CbFLP20Am4oI8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
[Neelesh Salian – Floe: Policy-Based Table Maintenance for Apache Iceberg](https://www.youtube.com/watch?v=UN44R8jYSXk)
///

![](https://raw.githubusercontent.com/nssalian/floe/refs/heads/main/docs/assets/architecture.png)
/// caption
architecture overview
///

![](https://nssalian.github.io/floe/assets/dashboard.png)

![](https://nssalian.github.io/floe/assets/policies.png)


## LakeOps

https://lakeops.dev/
