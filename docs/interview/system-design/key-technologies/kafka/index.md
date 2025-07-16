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

!!! question "What are the differences between Apache Kafka and Apache Pulsar?"

    ??? tip "Answer"

        Apache Kafka and Apache Pulsar differ mainly in architecture, message storage, and feature sets:

        **Kafka** uses a monolithic architecture where brokers handle both storage and serving. It stores messages in local disk files and relies on tools like ZooKeeper (or KRaft) for metadata. **Pulsar**, in contrast, has a decoupled architecture: brokers handle ingestion and dispatch, while BookKeeper handles durable storage, enabling better scalability and tiered storage support out of the box.

        **Pulsar** natively supports multi-tenancy, geo-replication, and topic-level message-level acknowledgment, while **Kafka** often requires external tools for those. However, Kafka has broader ecosystem support and is more mature in terms of community, integrations, and operational familiarity.

!!! question "What Is 2 Phase Commit (2PC) in Kafka?"

    ??? tip "Answer"

        In Kafka, **the Two-Phase Commit (2PC) is used to achieve exactly-once semantics (EOS) across Kafka** and an external system (like Flink or a database). Kafka supports this via its **transactional API**, which allows a producer to write to multiple partitions atomically.

        **Phase 1 (Prepare)**: The producer sends data and marks it as part of a transaction. Kafka buffers these messages but **doesn't expose them to consumers yet**.

        **Phase 2 (Commit or Abort)**: Once all messages are sent, the producer issues a commit or abort. Kafka then either makes all messages visible atomically or discards them.

        This mechanism ensures consistency but adds complexity and overhead, so it's used only when strict EOS is required.

!!! question "What is in-sync replication (ISR) in Kafka?"

    ??? tip "Answer"

        In Kafka, the In-Sync Replicas (ISR) are the set of replicas that are fully caught up with the leader for a given partition. They have received and acknowledged all messages the leader has committed. Kafka only considers a write successful when it's replicated to all brokers in the ISR set.

        ISR is critical for fault tolerance and exactly-once or at-least-once delivery guarantees. If the leader fails, Kafka will elect a new leader from the ISR to ensure no committed messages are lost. Replicas that fall behind too much are removed from the ISR until they catch up.