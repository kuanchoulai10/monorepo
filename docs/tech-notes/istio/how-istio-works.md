---
tags:
  - Istio
  - Service Mesh
  - How It Works
---

# How Istio Works

- `Istio Ingress Gateway` is a key component that manages external access to the services within the mesh. It acts as a reverse proxy, routing incoming traffic to the appropriate service based on the defined rules.
- `Istiod` is the control plane component of Istio, responsible for managing the configuration and policy for the service mesh. It handles the distribution of configuration to the data plane proxies and provides APIs for managing the mesh.
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