# Kafka

<iframe width="560" height="315" src="https://www.youtube.com/embed/DU8o-OTeoCc?si=RA3p-h8q6szboXDY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- [Kafka | Hello Interview](https://www.hellointerview.com/learn/system-design/deep-dives/kafka)

!!! question "What is Apache Kafka?"

    ??? tip "Answer"

        Apache Kafka is an open-source distributed event streaming platform. It's designed to handle real-time data feeds, allowing you to publish, subscribe to, store, and process streams of records in a **fault-tolerant** way. It's often used for building **real-time data pipelines**, **streaming applications**, and **event-driven architectures**. It was originally developed by LinkedIn and later became part of the Apache Software Foundation.


!!! question "What's the difference between Apache Kafka and the Message Queue?"

    ??? tip "Answer"

        Apache Kafka and traditional message queues, like RabbitMQ, both deal with messaging, but they have different architectures and use cases.
        
        Kafka is designed for high-throughput, distributed event streaming and can handle huge volumes of data with fault tolerance and scalability in mind. It uses a distributed log as its storage layer, which allows it to retain messages for a configurable amount of time, making it great for reprocessing and long-term storage of events.
        
        Traditional message queues, on the other hand, are usually designed for simpler point-to-point or pub-sub scenarios with a focus on delivering messages to consumers as quickly as possible, and they might not have the same level of built-in storage or scalability as Kafka.

