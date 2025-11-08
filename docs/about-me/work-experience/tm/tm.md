# Sr. Engineer, TM

??? note "About TM"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## XDR Lakehouse Project (Apache Iceberg + Trino)

The XDR (Extended Detection and Response) system serves as the backbone for collecting and analyzing security data from multiple endpoints including email servers, network devices, cloud services, and laptops. This massive dataset enables SOC teams to perform comprehensive threat detection and response across the organization's entire digital infrastructure.

The project focused on transitioning away from expensive, vendor-locked proprietary data platforms toward a modern open-source lakehouse architecture. By adopting **Trino** as the distributed query engine and **Apache Iceberg** as the table format, the team achieved significant cost reductions while gaining greater flexibility and control over large-scale data analytics operations.

!!! success "Key Achievements"

    - [x] **Engineered** production traffic mirroring system capable of handling 200 QPS during peak hours, migrating API request logs from Azure Application Insights to AWS SQS with CloudFormation-deployed architecture for traffic sampling, routing, and rate limiting
    - [x] **Integrated** Karpenter for EKS dynamic autoscaling, achieving improved resource utilization and cost reduction
    - [x] **Configured** KEDA for Trino auto-scaling based on query queue length, enabling dynamic worker adjustment
    - [x] **Implemented** point-in-time traffic replay functionality enabling consistent benchmark comparisons and continuous identification of peak-time performance bottlenecks
    - [x] **Optimized** Trino performance by reducing concurrent query limits, eliminating coordinator resource contention and improving overall query execution efficiency
    - [x] **Deployed** Fluent Bit logging infrastructure on EKS to capture comprehensive Trino query execution metrics (success/failure rates, execution times) and stream to CloudWatch for real-time monitoring
    - **Built** comprehensive CloudWatch monitoring dashboards tracking request forwarding success rates, failure rates, and latency metrics to ensure new architecture stability under production workloads


[Work Experience :material-page-previous-outline:{ .lg .middle }](../index.md){ .md-button }