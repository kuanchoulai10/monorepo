---
tags:
  - Apache Spark
  - Apache Flink
  - Streaming Processing
---
# Streaming Processing Window Types

## time

- Event time
- Arrival time
- Processing time


## Window Types

- **Tumbling Windows**
    - Flink: A tumbling windows assigner assigns each element to a window of a specified window size. Tumbling windows have a fixed size and do not overlap.
    - Spark: Tumbling windows are a series of fixed-sized, non-overlapping and contiguous time intervals. An input can only be bound to a single window.
- **Sliding Windows**
    - Flink: The sliding windows assigner assigns elements to windows of fixed length. Similar to a tumbling windows assigner, the size of the windows is configured by the window size parameter. An additional window slide parameter controls how frequently a sliding window is started. Hence, sliding windows can be overlapping if the slide is smaller than the window size. In this case elements are assigned to multiple windows.
    - Spark: Sliding windows are similar to the tumbling windows from the point of being "fixed-sized", but windows can overlap if the duration of slide is smaller than the duration of window, and in this case an input can be bound to the multiple windows.
- **Session Windows**
    - Flink: The session windows assigner groups elements by sessions of activity. Session windows do not overlap and do not have a fixed start and end time
    - Spark: Session window has a dynamic size of the window length, depending on the inputs. A session window starts with an input, and expands itself if following input has been received within static or dynamic gap duration.
- **Global Windows**

![Apache Spark Window Types](https://spark.apache.org/docs/latest/img/structured-streaming-time-window-types.jpg)

![Apache Flink Tumbling Windows](https://nightlies.apache.org/flink/flink-docs-release-2.0/fig/tumbling-windows.svg)

![Apache Flink Sliding Windows](https://nightlies.apache.org/flink/flink-docs-release-2.0/fig/sliding-windows.svg)

![Apache Flink Session Windows](https://nightlies.apache.org/flink/flink-docs-release-2.0/fig/session-windows.svg)

![Apache Flink Global Windows](https://nightlies.apache.org/flink/flink-docs-release-2.0/fig/non-windowed.svg)
