# Kafka

<iframe width="560" height="315" src="https://www.youtube.com/embed/DU8o-OTeoCc?si=RA3p-h8q6szboXDY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/Ajz6dBp_EB4?si=aPS8eQXJjfnBKjW9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- [Kafka | Hello Interview](https://www.hellointerview.com/learn/system-design/deep-dives/kafka)

!!! question "What is Apache Kafka?"

    ??? tip "Answer"

        Apache Kafka is an **open-source distributed event streaming platform**. It's designed to handle real-time data feeds, allowing you to publish, subscribe to, store, and process streams of records in a **fault-tolerant** way. It's often used for building **real-time data pipelines**, **streaming applications**, and **event-driven architectures**. It was originally developed by LinkedIn and later became part of the Apache Software Foundation.


!!! question "What's the difference between Apache Kafka and RabbitMQ?"

    ??? tip "Answer"

        There are quite a few differences between Kafka and RabbitMQ!

        For starters, **Kafka** is a *distributed event streaming platform*, while **RabbitMQ** is a *traditional message broker*.

        In terms of **storage**, **Kafka** is built around the concept of a *distributed commit log*, which means all the messages are stored on disk in a *durable*, *append-only* fashion. This design allows Kafka to *handle huge amounts of data* and retain messages for long periods, which is great for scenarios where you might want to *replay* or *reprocess* data. **RabbitMQ**, on the other hand, focuses more on *transient message delivery*, and while it does have persistent storage options, it's generally optimized for *ensuring that messages are delivered quickly to consumers rather than storing them for long-term replay*.

        In terms of **fault tolerance**, **Kafka** is designed with *replication in mind*, so it can handle node failures gracefully. **RabbitMQ** also supports clustering and mirrored queues for fault tolerance, but *it's not as inherently scalable as Kafka*.

        And when it comes to **consuming messages**, **Kafka** consumers **pull** messages from a partitioned log, which allows them to reprocess messages if needed. **RabbitMQ** consumers, however, typically get messages **pushed** to them, which can be more straightforward for certain use cases.

        **After a message is consumed**, the behavior differs quite a bit between Kafka and RabbitMQ. In **Kafka**, consuming a message doesn't actually remove it from the queue. Instead, the message remains in the log for a configured retention period, and the consumer just keeps track of its own offset, which is basically a pointer to where it last read. This means that multiple consumers can read the same message at different times, and you can even rewind or reprocess messages if needed. In **RabbitMQ**, once a message is consumed and acknowledged, it's typically removed from the queue, so it's more of a one-time delivery model.
