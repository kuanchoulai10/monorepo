---
tags:
  - Istio
  - Service Mesh
  - How It Works
---

# How Istio Works

## Core Components

- `Istio Ingress Gateway` is a key component that manages external access to the services within the mesh. It acts as a **reverse proxy**, routing incoming traffic to the appropriate service based on the defined rules.
- `Istiod` is the **control plane component of Istio**, responsible for managing the configuration and policy for the service mesh. It handles the distribution of configuration to the data plane proxies and provides APIs for managing the mesh. See [here](https://istio.io/latest/docs/ops/deployment/architecture/#istiod) for more details.

![](https://istio.io/latest/docs/ops/deployment/architecture/arch.svg)
/// caption
Istio Architecture
///

Along with creating a service mesh, Istio allows you to manage **gateways**, which are **Envoy proxies running at the edge of the mesh, providing fine-grained control over traffic entering and leaving the mesh**.


## 2 Main Data Plane Modes

A Istio Service Mesh can be logically divided into two parts: the **data plane** and the **control plane**.

The **data plane** consists of a set of proxies that mediate and control all network communication between services in the mesh.

The **control plane** is responsible for managing and configuring the proxies to route traffic, enforce policies, and collect telemetry.

Istio supports 2 main **data plane modes**:

- **Sidecar mode**: each pod has its own sidecar proxy (Envoy) that intercepts and manages traffic for that pod.
- **Ambient mode**: it uses a per-node Layer 4 proxy (Envoy) to handle traffic for all pods on that node and optionally a per-namespace Layer 7 proxy to provide additional features like traffic routing and telemetry.

### Sidecar Mode

### Ambient Mode

For Istio Ambient mode, it relies on `ztunnel` (Zero Trust Tunnel) to provide L4

![](https://istio.io/latest/docs/ambient/architecture/control-plane/ztunnel-architecture.svg)
/// caption
ztunnel architecture
///

![](https://istio.io/latest/docs/ambient/architecture/data-plane/ztunnel-waypoint-datapath.png)

## Deployment Models

See [here](https://istio.io/latest/docs/ops/deployment/deployment-models/) for more details on different deployment models supported by Istio.

### Cluster Models

#### Single cluster

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-cluster.svg)
/// caption
A service mesh with a single cluster
///

#### Multiple clusters

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-cluster.svg)
/// caption
A service mesh with multiple clusters
///

#### DNS with multiple clusters

### Network Models

#### Single network

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-net.svg)
/// caption
A service mesh with a single network
///

#### Multiple networks

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-net.svg)
/// caption
A service mesh with multiple networks
///

### Control Plane Models

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-cluster.svg)
/// caption
A single cluster with a control plane
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/shared-control.svg)
/// caption
A service mesh with a primary and a remote cluster
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-cluster-external-control-plane.svg)
/// caption
A single cluster with an external control plane
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/endpoint-discovery.svg)
/// caption
Primary clusters with endpoint discovery
///

### Identity and trust models

![](https://istio.io/latest/docs/ops/deployment/deployment-models/single-trust.svg)
/// caption
A service mesh with a common certificate authority (Trust within a mesh)
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-trust.svg)
/// caption
Multiple service meshes with different certificate authorities (Trust between meshes)
///

### Mesh models

#### Single mesh


#### Multiple meshes

![](https://istio.io/latest/docs/ops/deployment/deployment-models/multi-mesh.svg)
/// caption
Multiple service meshes
///

### Tenancy models

#### Namespace tenancy

![](https://istio.io/latest/docs/ops/deployment/deployment-models/exp-ns.svg)
/// caption
A service mesh with two namespaces and an exposed service
///

![](https://istio.io/latest/docs/ops/deployment/deployment-models/cluster-ns.svg)
/// caption
A service mesh with clusters with the same namespace
///
#### Cluster tenancy

#### Mesh tenancy

![](https://istio.io/latest/docs/ops/deployment/deployment-models/cluster-iso.svg)
/// caption
Two isolated service meshes with two clusters and two namespaces
///

## CRDs

Istio introduces several Custom Resource Definitions (CRDs) to manage and configure the service mesh. Some of the key CRDs include:

- **VirtualService**: Defines how requests are routed to services within the mesh.
- **DestinationRule**: Configures policies for traffic to a service after routing has occurred
- **Gateway**: Manages ingress and egress traffic for the mesh.

Other CRDs include `ServiceEntry`, `Sidecar`, and `AuthorizationPolicy`, etc.

### Gateway

The `Gateway` CRD allows you to configure how traffic enters and exits the service mesh. It defines ports, protocols, and hosts for incoming and outgoing traffic. This is not about deploying a physical gateway but rather configuring the behavior of the Istio Ingress Gateway.

### VirtualService

The `VirtualService` CRD is used to define the routing rules for traffic within the service mesh. It allows you to specify how requests to a service are handled, including routing based on HTTP headers, URI paths, or other criteria. This enables advanced traffic management features such as A/B testing, canary releases, and traffic splitting.

### DestinationRule

The `DestinationRule` CRD is used to configure policies that apply to traffic after it has been routed to a service. This includes settings for load balancing, connection pool sizes, outlier detection, and circuit breaking. DestinationRules work in conjunction with VirtualServices to provide fine-grained control over traffic behavior.

### Traffic Flow

Making it all work together, when a request is made to a service within the mesh, the following sequence occurs:

1. The request first hits the **Istio Ingress Gateway** if it is coming from outside the mesh.
2. The `Gateway` configuration determines how to handle the incoming request.
3. The request is then routed to the appropriate service based on the rules defined in the `VirtualService`.
4. Once the request reaches the service, the `DestinationRule` policies are applied to manage traffic behavior.