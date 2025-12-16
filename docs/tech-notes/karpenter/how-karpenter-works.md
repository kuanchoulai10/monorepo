---
tags:
  - Karpenter
  - How It Works
---

# How Karpenter Works

## Concepts

### NodeClasses

### NodePools

### NodeClaims

### NodeOverlays

### Scheduling

### Disruption

consolidation, drift, and expiration

## From the Cluster Administrator's and Application Developer's Perspectives

### Cluster Administrator

- Installing Karpenter
- Configuring `NodePools`
    - Karpenter only attempts to schedule pods that have a status condition `Unschedulable=True`
    - Karpenter defines a Custom Resource called a `NodePool` to specify configuration
    - A `NodePool` can also include values to indicate when nodes should be disrupted.
    - The NodePool can use well-known Kubernetes labels to allow pods to request only certain instance types, architectures, operating systems, or other attributes when creating nodes.
    - Multiple `NodePools` can be configured on the same cluster. For example, you might want to configure **different teams on the same cluster to run on completely separate capacity**.
- Disrupting nodes
    - Finalizer: Karpenter places a **finalizer** bit on each node it creates. When a request comes in to delete one of those nodes, Karpenter will cordon the node, drain all the pods, terminate the EC2 instance, and delete the node object.
    - Expiration: Karpenter will mark nodes as expired and disrupt them after they have lived a set number of seconds
    - Consolidation: Karpenter works to actively reduce cluster cost by identifying when
        - the node is empty
        - their workloads will run on other nodes in the cluster
        - Nodes can be replaced with cheaper variants due to a change in the workloads.
    - Drift
    - Interruption
- Scheduling: Karpenter launches nodes in response to pods that the Kubernetes scheduler has marked unschedulable.

### Application Developer

- `nodeAffinity`
- `topologySpreadConstraints`
- `nodeSelector`
- `resource.requests`

When Karpenter tries to provision a node, it analyzes scheduling constraints before choosing the node to create.

As long as the requests are not outside the NodePool’s constraints, Karpenter will look to best match the request, comparing the same well-known labels defined by the pod’s scheduling constraints.
## Why Karpenter Instead of Cluster Autoscaler?

- **Built for comprehensive cloud flexibility**: Karpenter can effectively manage the complete spectrum of AWS instance options. In contrast, the cluster autoscaler wasn't initially designed to accommodate the vast array of instance types, availability zones, and purchasing models that AWS offers.
- **Rapid instance deployment**: Karpenter handles instances individually through **direct management** rather than relying on intermediate coordination layers such as node groups. This approach allows for **rapid retry attempts within milliseconds when resources are unavailable**, compared to the minutes required by other solutions. Additionally, this direct management enables Karpenter to utilize a wide variety of instance types, availability zones, and purchasing strategies without needing to establish numerous node groups.

## Comparison with Cluster Autoscaler

![](./assets/comparisons.excalidraw.svg)