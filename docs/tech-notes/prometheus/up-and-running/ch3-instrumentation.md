---
tags:
  - SRE
  - Prometheus
---

# Ch3 Instrumentation

## Glossary

### Counter

: *Counters are the type of metric you will probably use most often in instrumentation. Counters track either the number or size of events. They are mainly used to track how often a particular code path is executed.*

### Gauge

: *Gauges are a snapshot of some current state*

### Summary

: *A Prometheus Summary is used to track request latencies by recording the total count, sum and then you can calculate average latency. `Summary.observe(value)` and `@Summary.time()` are the two main methods to use a Summary.*

### Histogram

: *Just like a Summary, a Histogram is used to track request latencies. The main difference is that a Histogram tracks the count of observations that fall into configurable **buckets**, allowing you to see the distribution of latencies. The best way to think of buckets (and metrics generally) is that while they may not always be perfect, they generally give you sufficient information to determine the next step when you are debugging*

## Notes

- We recommend **debugging latency issues primarily with averages** rather than quantiles.