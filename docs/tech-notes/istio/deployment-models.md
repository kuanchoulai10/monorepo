---
tags:
  - Istio
  - Service Mesh
---

# Deployment Models

See [here](https://istio.io/latest/docs/ops/deployment/deployment-models/) for more details on different deployment models supported by Istio.

## Cluster Models

### Single cluster

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-cluster.svg){ width="500" }
/// caption
[A service mesh with a single cluster](https://istio.io/latest/docs/ops/deployment/deployment-models/#single-cluster)
///

### Multiple clusters

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-cluster.svg){ width="500" }
/// caption
[A service mesh with multiple clusters](https://istio.io/latest/docs/ops/deployment/deployment-models/#multiple-clusters)
///

### DNS with multiple clusters

## Network Models

### Single network

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-net.svg){ width="500" }
/// caption
[A service mesh with a single network](https://istio.io/latest/docs/ops/deployment/deployment-models/#single-network)
///

### Multiple networks

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-net.svg){ width="500" }
/// caption
[A service mesh with multiple networks](https://istio.io/latest/docs/ops/deployment/deployment-models/#multiple-networks)
///

## Control Plane Models

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-cluster.svg){ width="500" }
/// caption
[A single cluster with a control plane](https://istio.io/latest/docs/ops/deployment/deployment-models/#control-plane-models)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/shared-control.svg){ width="500" }
/// caption
[A service mesh with a primary and a remote cluster](https://istio.io/latest/docs/ops/deployment/deployment-models/#control-plane-models)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-cluster-external-control-plane.svg){ width="500" }
/// caption
[A single cluster with an external control plane](https://istio.io/latest/docs/ops/deployment/deployment-models/#control-plane-models)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-control.svg)
/// caption
[A service mesh with control plane instances for each region](https://istio.io/latest/docs/ops/deployment/deployment-models/#control-plane-models)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/endpoint-discovery.svg){ width="500" }
/// caption
[Primary clusters with endpoint discovery](https://istio.io/latest/docs/ops/deployment/deployment-models/#endpoint-discovery-with-multiple-control-planes)
///

## Identity and trust models

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-trust.svg){ width="500" }
/// caption
[A service mesh with a common certificate authority (Trust within a mesh)](https://istio.io/latest/docs/ops/deployment/deployment-models/#trust-within-a-mesh)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-trust.svg){ width="500" }
/// caption
[Multiple service meshes with different certificate authorities (Trust between meshes)](https://istio.io/latest/docs/ops/deployment/deployment-models/#trust-between-meshes)
///

## Mesh models

### Single mesh


### Multiple meshes

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-mesh.svg){ width="500" }
/// caption
[Multiple service meshes](https://istio.io/latest/docs/ops/deployment/deployment-models/#multiple-meshes)
///

## Tenancy models

### Namespace tenancy

![](https://istio.io/latest/docs/ops/deployment/deployment-models/exp-ns.svg){ width="500" }
/// caption
[A service mesh with two namespaces and an exposed service](https://istio.io/latest/docs/ops/deployment/deployment-models/#namespace-tenancy)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/cluster-ns.svg){ width="500" }
/// caption
A service mesh with clusters with the same namespace
///
### Cluster tenancy

### Mesh tenancy

![](https://istio.io/latest/docs/ops/deployment/deployment-models/cluster-iso.svg){ width="500" }
/// caption
[Two isolated service meshes with two clusters and two namespaces](https://istio.io/latest/docs/ops/deployment/deployment-models/#mesh-tenancy)
///