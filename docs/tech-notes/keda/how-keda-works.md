---
tags:
  - Keda
---

# How KEDA Works

> *KEDA monitors **external event sources** and adjusts your app's resources based on the demand.*

## Components

### KEDA Operator

: keeps track of event sources and changes the number of app instances up or down, depending on the demand.

### Metrics Server

: provides external metrics to Kubernetes' HPA so it can make scaling decisions.

### Scalers

: connect to event sources like message queues or databases, pulling data on current usage or load.

### CRDs

: define how your apps should scale based on triggers like queue length or API request rates. `ScaledObject` and `ScaledJob` are the main CRDs used to configure scaling behavior. `TriggerAuthentication` is used to securely store authentication details for connecting to external systems.



## References

- [KEDA Concepts](https://keda.sh/docs/2.18/concepts/)
