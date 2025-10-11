---
tags:
  - SRE
  - Prometheus
---

# Ch5 Labels

- Labels are key-value pairs associated with time series that, in addition to the metric name, uniquely identify them.
- Labels come from two sources, *instrumentation labels* and *target labels*.
    - *Instrumentation labels*, as the name indicates, come from your instrumentation. They are about things that are known inside your application or library
    - *Target labels* identify a specific monitoring target; that is, a target that Prometheus scrapes. It comes from *service discovery* and *relabeling*.

```
# TYPE latency_seconds summary
latency_seconds                  # metric family
latency_seconds{path="/bar"}     # metric child
latency_seconds_sum{path="/bar"} # time series

```