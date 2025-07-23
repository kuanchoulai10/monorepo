---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-07-29
  updated: 2025-07-29
categories:
  - Data
links:
  - How Agoda manages 1.8 trillion Events per day on Kafka: https://medium.com/agoda-engineering/how-agoda-manages-1-8-trillion-events-per-day-on-kafka-1d6c3f4a7ad1
  - Scaling Kafka to Support PayPal's Data Growth: https://medium.com/paypal-tech/scaling-kafka-to-support-paypals-data-growth-a0b4da420fab
  - Revolutionizing Real-Time Streaming Processing - 4 Trillion Events Daily at LinkedIn: https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event
  - Reliably Processing Trillions of Kafka Messages Per Day | Walmart: https://medium.com/walmartglobaltech/reliably-processing-trillions-of-kafka-messages-per-day-23494f553ef9
  - The Trillion Message Kafka Setup at Walmart | ByteByteGo: https://blog.bytebytego.com/p/the-trillion-message-kafka-setup
  - Best practices for scaling Apache Kafka | New Relic: https://newrelic.com/blog/best-practices/kafka-best-practices
  - Handling 2 Million Apache Kafka Messages Per Second at Honeycomb | Honeycomb Blog: https://developer.confluent.io/learn-more/podcasts/handling-2-million-apache-kafka-messages-per-second-at-honeycomb/
tags:
  - Apache Kafka
comments: true
hide:
  - toc
---

# Apache Kafka in Production: Insights from Big Companies

!!! info "TLDR"

    After reading this article, you will learn:

    - abc
    - def
    - ghi


<!-- more -->

前陣子剛開始接觸 Apache Kafka，除了在學習那些基礎觀念和實作外，也想了解一下大公司是如何使用 Apache Kafka 的，於是這篇文章就誕生了。這篇文章就會分享一些大公司使用 Apache Kafka 的案例，並且提供一些相關的資源。

- [Agoda](#agoda)
- [PayPal](#paypal)
- [LinkedIn](#linkedin)
- [Walmart](#walmart)
- [Honeycomb](#honeycomb)

## Agoda

[How Agoda manages 1.8 trillion Events per day on Kafka](https://medium.com/agoda-engineering/how-agoda-manages-1-8-trillion-events-per-day-on-kafka-1d6c3f4a7ad1)

This article was published in 2023, sharing Agoda's experience with Apache Kafka since 2015. Agoda currently processes approximately 1.8 trillion events per day with an average year-over-year growth rate of 2x. Their Kafka use cases have expanded from initial analytical data pipelines to asynchronous APIs, cross-data center replication, and data feeding for machine learning pipelines. The article mentions they use multiple smaller Kafka clusters instead of a single large cluster, and 85% of developers use their 2-Step architecture to send data.

As Kafka usage scaled rapidly, Agoda faced numerous challenges that needed to be addressed. These challenges primarily revolved around maintaining system reliability, scalability, and operability while ensuring development teams could effectively use Kafka without needing deep understanding of its complexity. Below are the seven main challenges they encountered during their Kafka infrastructure evolution:

- Simplifying how developers send data to Kafka
- Designing appropriate Kafka cluster architecture
- Establishing monitoring and auditing mechanisms to ensure data integrity
- Determining when to scale Kafka clusters
- Managing data growth and attributing costs to teams
- Implementing authentication and access control
- Providing automated tools to improve operational efficiency

### 2-Step Logging Architecture: Solving Development Complexity

**Problem**

Development teams needing to interact directly with Kafka increases complexity and makes operational management difficult.

**Solution**

Adopted a 2-Step architecture - client libraries write events to disk, and an independent Forwarder daemon reads and forwards them to Kafka.

**Benefits**

- Separates operational concerns from development teams
- Simplifies API and enforces serialization standards
- Increases resilience
- Allows Kafka team to independently perform configuration, upgrades, and optimizations

**Drawbacks**

- Increases latency (99th percentile of 10 seconds)
- Adds architectural complexity
- Requires maintaining Forwarder processes on every node

**Trade-offs**

Accepts increased latency for better resilience and flexibility. For critical applications requiring sub-second latency, direct Kafka Client usage is still available.

### Multiple Small Clusters: Risk Isolation and Customization

**Problem**

A single large cluster could affect all applications and is difficult to optimize for different use cases.

**Solution**

Split into multiple small Kafka clusters based on use cases rather than having one large cluster per data center.

**Benefits**

- Isolates the impact scope of potential issues
- Allows different hardware specs and configurations for different use cases
- Enables transparent event routing to different clusters via Forwarder

**Drawbacks**

- Increases management complexity
- Requires maintaining multiple clusters

**Trade-offs**

Accepts increased management complexity for better isolation and flexibility. Also provides dedicated physical nodes and SSD disks for Zookeeper.

### Monitoring and Auditing: Building Trust and Visibility

**Problem**

Kafka Broker statistics alone are insufficient to ensure data completeness, reliability, and timeliness.

**Solution**

Implemented comprehensive monitoring (JMXTrans + Graphite + Grafana) and auditing systems, asynchronously aggregating message counts in client libraries.

**Benefits**

- Provides end-to-end data visibility
- Ability to track event counts across different pipeline stages
- Facilitates troubleshooting and SLA monitoring

**Drawbacks**

- Increases system complexity
- Requires an additional Kafka cluster to store audit information

**Trade-offs**

Accepts additional infrastructure costs and complexity for data trust and visibility.

### Capacity Planning: Comprehensive Scaling Metrics

**Problem**

Using only disk usage as a scaling metric is inaccurate since Kafka retention can be dynamically configured.

**Solution**

Developed a comprehensive capacity calculation method considering CPU, network, disk, partition count, and other resource metrics, taking the highest percentage as overall capacity.

**Benefits**

- Provides more accurate capacity assessment
- Identifies primary resource bottlenecks
- Aids scaling and downsizing decisions

**Drawbacks**

Requires setting and maintaining upper limits for multiple monitoring metrics.

**Trade-offs**

Accepts increased monitoring complexity for more accurate capacity planning.

### Cost Attribution: Incentivizing Responsible Data Usage

**Problem**

The data platform became a dumping ground where much of the sent/stored data wasn't generating value.

**Solution**

Attributed monetary value to teams based on bytes sent, with each Kafka topic having a responsible team.

**Benefits**

- Incentivizes teams to evaluate data needs
- Transforms cost management mindset
- Promotes responsible resource usage

**Drawbacks**

- Requires establishing cost calculation models
- May impact data democratization

**Trade-offs**

Deliberately ignores consumer usage to avoid penalizing data consumption, focusing on producer responsibility.

### Authentication and Access Control: Security and Compliance

**Problem**

- Unable to identify and handle users abusing Kafka
- Need to restrict access to specific topics

**Solution**

Implemented Kafka Authentication & Authorization system in 2021, including self-service credential and ACL request mechanisms.

**Benefits**

- Enables user management and credential expiration settings
- Provides topic access control
- Prevents sensitive data leaks

**Drawbacks**

- Increases system complexity
- May impact performance (especially after adding SSL encryption)

**Trade-offs**

Accepts potential performance impact for security and compliance, currently testing certificate authentication and SSL encryption.

### Automated Tools: Operational Scalability

**Problem**

As more Kafka clusters are managed, better tools are needed to ensure operational process scalability.

**Solution**

Uses a mix of open-source tools (like Cruise Control, Kafka UI) and internally developed tools for binary deployments, broker configuration propagation, and rolling restarts.

**Benefits**

- Improves operational efficiency
- Reduces manual operations
- Supports large-scale management

**Drawbacks**

Requires continuous investment in tool development and maintenance.

**Trade-offs**

Recognizes this as a necessary part of large-scale system management, continuously seeking and developing better tools.

## PayPal

[Scaling Kafka to Support PayPal's Data Growth](https://medium.com/paypal-tech/scaling-kafka-to-support-paypals-data-growth-a0b4da420fab)

This article was published in 2023, sharing PayPal's experience with Apache Kafka since its introduction in 2015. PayPal currently operates over 85 Kafka clusters with more than 1,500 brokers hosting over 20,000 topics, processing over 100 billion messages per day across various use cases. During peak traffic like Black Friday 2022, their platform handled 1.3 trillion messages per day with 21 million messages per second, achieving 99.99% availability through close to 2,000 Mirror Maker nodes for cross-cluster data mirroring.

As PayPal's Kafka infrastructure scaled dramatically to support growing payment volumes, they encountered significant operational challenges. These challenges centered around maintaining high availability and security while reducing operational overhead for both the platform team and application developers. The complexity of managing multiple geographically distributed data centers, different security zones, and supporting over 800 applications with various tech stacks required sophisticated tooling and automation solutions.

The article highlights four key aspects of managing Kafka clusters at scale: Cluster Management, Monitoring and Alerting, Configuration Management, and Enhancements and Automation. Each area addresses specific operational challenges while balancing system reliability, developer experience, and maintenance overhead.

### Cluster Management

**Problem**

- Clients hardcoding broker IPs led to maintenance nightmares during upgrades, patching, or broker replacements
- Lack of standardized Kafka configurations across different clients resulted in support overhead and potential misconfigurations
- Security risks from allowing plain text connections and unrestricted topic access
- Need for production-like QA environment that matches security standards and cluster configurations

**Solution**

- Implemented Kafka Config Service as a highly available stateless service that provides bootstrap servers and standardized configurations
- Introduced Access Control Lists (ACLs) requiring SASL authentication and explicit producer/consumer permissions per topic
- Developed PayPal-specific client libraries including Resilient Client Library, Monitoring Library, and Security Library
- Built new QA platform on Google Cloud Platform with one-to-one mapping to production clusters and rack-aware deployment

**Benefits**

- Plug-and-play model for Kafka clients with automatic configuration updates
- Secure platform with controlled access and application tracking
- Reduced onboarding time and enhanced developer efficiency
- 75% cost reduction and 40% performance improvement in QA environment
- Automatic certificate management and key rotation handling

**Drawbacks**

- Additional infrastructure complexity with new services to maintain
- Potential single point of failure for the Config Service
- Increased authentication overhead for all client connections
- Need to maintain multiple client libraries across different tech stacks

**Trade-offs**

Accepts increased infrastructure complexity and maintenance overhead for significantly improved security, standardization, and operational efficiency. Prioritizes developer experience and platform stability over architectural simplicity.

### Monitoring and Alerting

**Problem**

Kafka provides extensive metrics out of the box, but identifying the right subset for effective monitoring at scale while minimizing alert noise and ensuring fast issue detection was challenging.

**Solution**

Implemented fine-tuned monitoring system using Micrometer registry and SignalFX backend, with filtered metrics from custom Kafka Metrics library running on all brokers, Zookeepers, MirrorMakers, and clients. Developed clear Standard Operating Procedures for every triggered alert.

**Benefits**

- Faster issue identification with reduced operational overhead
- Clear action procedures for SRE teams to resolve issues quickly
- Contributed open-source KIPs (351, 427, 517) to improve Kafka observability
- Comprehensive health monitoring across the entire Kafka ecosystem

**Drawbacks**

- Requires ongoing metric tuning and threshold adjustments
- Additional infrastructure for metrics collection and processing
- Need to maintain SOPs and keep them updated

**Trade-offs**

Accepts additional monitoring infrastructure costs and maintenance for critical visibility into platform health and rapid incident response capabilities.

### Configuration Management

**Problem**

Need for a single source of truth for entire Kafka infrastructure metadata including clusters, topics, and applications, especially for disaster recovery scenarios.

**Solution**

Implemented internal configuration management system storing all Kafka infrastructure metadata with frequent backups, serving as the authoritative source for rebuilding clusters and topics.

**Benefits**

- Single source of truth for resolving conflicts
- Ability to recreate clusters and topics within hours during recovery
- Complete infrastructure visibility and documentation

**Drawbacks**

- Additional system to maintain and backup
- Potential data inconsistency if not properly synchronized

**Trade-offs**

Accepts additional system complexity for critical disaster recovery capabilities and operational clarity.

### Enhancements and Automation

**Problem**

- Manual operational tasks don't scale with growing infrastructure
- Security vulnerabilities require frequent patching without causing data loss
- Topic and MirrorMaker onboarding processes need streamlining
- Default Kafka partition reassignment affects healthy brokers unnecessarily

**Solution**

- Built plugin for patching system to check under-replicated partition status before host restarts
- Contributed KIP-519 for extensible SSL context to meet PayPal security standards
- Automated topic onboarding with capacity analysis integration and automatic ACL creation
- Enhanced partition reassignment to only affect under-replicated partitions on affected brokers

**Benefits**

- Zero data loss during patching operations
- Streamlined onboarding workflows with integrated capacity planning
- Significantly reduced partition reassignment time from days to hours
- Automated security compliance and access control

**Drawbacks**

- Custom tooling requires ongoing development and maintenance
- Dependency on internal automation systems
- Complexity in coordinating multiple automated workflows

**Trade-offs**

Invests heavily in automation and custom tooling development to achieve operational scalability, accepting increased initial development effort for long-term operational efficiency and system reliability.

## LinkedIn

[Revolutionizing Real-Time Streaming Processing - 4 Trillion Events Daily at LinkedIn](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event)

This article was published in October 2023, sharing LinkedIn's experience with Apache Beam and streaming processing infrastructure. LinkedIn currently processes over 4 trillion events daily through more than 3,000 Apache Beam pipelines across multiple production data centers. Their streaming infrastructure serves over 950 million members and has achieved significant performance improvements including 2x cost optimization, processing acceleration from days to minutes for anti-abuse detection, and reduced time-to-production for new pipelines from months to days.

As LinkedIn scaled their data infrastructure to handle massive volumes of real-time data processing, they encountered significant operational challenges. These challenges centered around managing sophisticated streaming applications at scale while ensuring high performance, reliability, and developer productivity. The complexity of maintaining thousands of pipelines, supporting diverse use cases from machine learning to anti-abuse detection, and providing a unified platform for both streaming and batch processing required innovative solutions that could abstract operational complexity while delivering enterprise-grade performance.

The article highlights LinkedIn's approach to building a comprehensive streaming processing platform using Apache Beam, focusing on five key areas: Unified Streaming and Batch Pipelines, Anti-Abuse & Near Real-Time AI Modeling, Notifications Platform, Real-Time ML Feature Generation, and Managed Streaming Processing Platform. Each area demonstrates how Apache Beam's unified programming model addresses specific business requirements while maintaining operational excellence.

### Unified Streaming and Batch Pipelines

**Problem**

- Maintaining separate codebases for streaming and batch processing led to operational complexity and inefficiencies
- Backfilling operations as streaming jobs required over 5,000 GB-hours in memory and 4,000 CPU hours, causing extended processing times
- Resource-intensive backfilling acted as "noisy neighbors" to colocated streaming pipelines, failing to meet latency and throughput requirements
- Need for periodic backfilling when new AI models were introduced while maintaining real-time processing capabilities

**Solution**

- Adopted Apache Beam's unified programming model to implement business logic once that handles both real-time and batch processing
- Created custom composite transforms to abstract I/O differences and switch processing modes based on data source type
- Leveraged Apache Beam's "write once, run anywhere" capability to deploy the same pipeline on different engines (Samza for streaming, Spark for batch)
- Implemented PipelineOptions for runtime configuration and customization of processing behavior

**Benefits**

- Achieved 50% improvement in memory and CPU usage efficiency (from ~5,000 GB-hours to ~2,000 GB-hours)
- Reduced processing time by 94% (from 7.5 hours to 25 minutes) for backfilling operations
- Eliminated the need to maintain separate codebases for streaming and batch processing
- Enabled seamless switching between processing modes without code changes
- Achieved 2x cost optimization through unified architecture

**Drawbacks**

- Requires learning and adopting Apache Beam's programming model and abstractions
- Potential complexity in designing transforms that work efficiently across both streaming and batch modes
- Dependency on Apache Beam framework evolution and compatibility

**Trade-offs**

Accepts framework dependency and learning curve for significant operational efficiency gains and cost reduction. Prioritizes code maintainability and resource optimization over architectural simplicity, enabling teams to focus on business logic rather than infrastructure management.

### Anti-Abuse & Near Real-Time AI Modeling

**Problem**

- Detection and prevention of platform abuse (fake accounts, scraping, spam) required near real-time processing capabilities
- Traditional batch processing took up to 1 day to label abusive actions, allowing malicious activities to continue undetected
- Need to process time-series events at massive scale while maintaining low latency for immediate threat response
- Complex AI model integration required sophisticated event filtering, aggregation, and scoring capabilities

**Solution**

- Built Chronos anti-abuse platform with two streaming Apache Beam pipelines: Filter pipeline and Model pipeline
- Filter pipeline reads user activity events from Kafka, extracts relevant fields, aggregates and filters events for downstream processing
- Model pipeline consumes filtered messages, aggregates member activity within time windows, triggers AI scoring models, and writes abuse scores to internal systems
- Leveraged Apache Beam's pluggable architecture and I/O connectors for seamless integration with Kafka and key-value stores

**Benefits**

- Reduced abuse detection time from 1 day to 5 minutes, enabling near real-time threat response
- Achieved processing of time-series events at over 3 million queries per second
- Improved detection of logged-in scraping profiles by more than 6%
- Enhanced overall platform security with 21% improvement in fake account detection and 15% improvement in scraping detection

**Drawbacks**

- Increased infrastructure complexity with multiple interconnected streaming pipelines
- Higher operational overhead for monitoring and maintaining real-time AI model scoring
- Potential latency impact from complex event aggregation and AI model inference

**Trade-offs**

Accepts increased system complexity and operational overhead for critical security improvements and member protection. Prioritizes platform safety and user trust over architectural simplicity, enabling proactive threat detection and rapid response capabilities.

### Notifications Platform

**Problem**

- Need to generate and distribute personalized notifications to over 950 million LinkedIn members in near real-time
- Complex business logic required for processing enormous volumes of member activity data
- Machine learning models needed to perform distributed targeting and scoring of millions of candidate notifications per second
- Requirement for timely, relevant, and actionable notifications across multiple channels

**Solution**

- Implemented streaming Apache Beam pipelines with intricate business logic to handle massive data volumes
- Built pipelines that consume, aggregate, partition, and process events from all LinkedIn members
- Integrated with downstream machine learning models for personalized notification targeting and scoring
- Leveraged Apache Beam's advanced aggregation and filtering capabilities for complex event processing

**Benefits**

- Enabled scalable, near real-time infrastructure for business-critical member engagement
- Provided out-of-the-box complex aggregation and filtering capabilities
- Created reusable components through Apache Beam's programming model
- Accelerated development and streamlined scaling as more notification use cases migrated from Samza to Beam

**Drawbacks**

- High complexity in managing intricate business logic across multiple streaming pipelines
- Significant computational resources required for processing events from 950+ million members
- Operational overhead in maintaining ML model integration and scoring systems

**Trade-offs**

Accepts high computational costs and operational complexity for critical member engagement capabilities. Prioritizes user experience and platform growth over resource efficiency, enabling personalized and timely communication that drives member activity and platform value.

### Real-Time ML Feature Generation

**Problem**

- Original offline ML feature generation suffered from 24-48 hour delays between member actions and recommendation system updates
- Delayed feature updates resulted in missed opportunities for infrequent members and failed to capture short-term intent of frequent members
- Need for scalable, real-time ML feature generation platform to support job recommendations and search feed functionalities
- Complex integration requirements between feature generation, storage, and recommendation systems

**Solution**

- Developed hosted platform for ML feature generation using Managed Beam as foundation
- Created streaming Apache Beam pipelines that filter, process, and aggregate events emitted to Kafka in real-time
- Implemented additional pipelines for retrieving data from feature store, processing it, and feeding into recommendation systems
- Provided AI engineers with efficient pipeline authoring experience while abstracting deployment and operational complexities

**Benefits**

- Eliminated 24-48 hour delay, achieving end-to-end pipeline latency of just a few seconds
- Enabled ML models to leverage up-to-date information for more personalized and timely recommendations
- Provided scalable platform that abstracts operational complexity for AI engineers
- Achieved significant gains in business metrics through improved recommendation quality

**Drawbacks**

- Increased infrastructure complexity with multiple integrated pipeline systems
- Higher operational costs for maintaining real-time feature generation and storage
- Dependency on managed platform availability and performance

**Trade-offs**

Accepts increased infrastructure investment and operational complexity for substantial improvements in recommendation quality and business metrics. Prioritizes user experience and platform effectiveness over cost efficiency, enabling data-driven personalization at scale.

### Managed Streaming Processing Platform

**Problem**

- Managing over 3,000 Apache Beam pipelines overwhelmed AI and data engineering teams with 24/7 operational responsibilities
- Complex integration of multiple streaming tools and infrastructures created development bottlenecks
- Limited infrastructure knowledge among AI engineers led to deployment, monitoring, and operational challenges
- Time-consuming pipeline development cycle often lasted one to two months, hindering business agility

**Solution**

- Created Managed Beam platform that streamlines and automates internal streaming application processes
- Developed custom workflow components as reusable sub-DAGs exposed as standard PTransforms
- Implemented central control plane with deployment UI, operational dashboard, administrative tools, and automated lifecycle management
- Built autosizing controller tool that automates hardware resource tuning and provides auto-remediation for streaming pipelines

**Benefits**

- Reduced time to author, test, and stabilize streaming pipelines from months to days
- Almost entirely eliminated operational costs for AI engineers through automation
- Enabled fully-automated autoscaling, significantly reducing manual "trial and error" iterations
- Provided log separation, multi-language API support, and automated framework upgrades

**Drawbacks**

- Significant investment required in developing and maintaining managed platform infrastructure
- Dependency on centralized control plane creates potential single point of failure
- Complexity in coordinating automated systems and ensuring reliable auto-remediation

**Trade-offs**

Invests heavily in platform development and automation infrastructure to achieve dramatic improvements in developer productivity and operational efficiency. Accepts increased initial development costs and system complexity for long-term scalability and reduced operational burden across engineering teams.

## Walmart