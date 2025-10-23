---
tags:
  - Karpenter
---

# Karpenter Best Practices

!!! success "Best Practices"

    - [x] Lock down AMIs in production clusters
    - [x] Use Karpenter for workloads with changing capacity needs
    - [x] Consider other autoscaling projects when you need features that are still being developed in Karpenter.
    - [x] Run the Karpenter controller on EKS Fargate or on a worker node that belongs to a node group
    - [x] No custom launch templates support with Karpenter
    - [x] Exclude instance types that do not fit your workload
    - [x] Enable Interruption Handling when using Spot
    - [x] Amazon EKS private cluster without outbound internet access
