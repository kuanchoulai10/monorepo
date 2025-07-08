# System Design Questions

## Core Concepts

- [x] [CAP Theorem](./cap.md)
- [x] [Consistent Hashing](./consistent-hashing.md)


## Key Technologies

- [x] [Apache Kafka](./kafka.md)
- [x] [AWS DynamoDB](./dynamodb.md)
- [ ] [Apache Spark](./spark.md)

## Product System Design

In these interviews, you'll be asked to design a system behind a product.

- [x] [Design a Ride-Sharing Service Like Uber](./ride-sharing-service.md)

## Infrastructure System Design

In these interviews, you'll be asked to design a system that supports a particular infrastructure use case.

- [x] [Design a Rate Limiter](./rate-limiter.md)
- [ ] [Design a Distributed Message Queue](./distributed-message-queue.md)

## Machine Learning System Design

In these interviews, you'll be asked to design a system that supports a particular machine learning use case.

## Data Pipeline Design

In these interviews, you'll be asked to design a system that supports a particular data pipeline use case.

## Data Modeling

In these interviews, you'll be asked to design a data model for a particular use case.

## Data Architecture

In these interviews, you'll be asked to design a data architecture for a particular use case.

### Core technologies

- [x] [Apache Spark](./spark.md)

---


!!! question "System Design Trade-Offs"

    ??? tip "Video"

        <iframe width="560" height="315" src="https://www.youtube.com/embed/1nENigGr-a0?si=1sv2c336Cch7k43L" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

        - SQL vs NoSQL
        - Normalization vs Denormalization
        - Consistency vs Availability
        - Strong Consistency vs Eventual Consistency
        - Batch Processing vs Stream Processing

        <iframe width="560" height="315" src="https://www.youtube.com/embed/2g1G8Jr88xU?si=njv5ki8NzLZq7N2F" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        
        - Vertical Scaling vs Horizontal Scaling
        - REST vs graphQL
        - Stateful vs Stateless
        - Read-through vs Write-through Caching
        - Sync vs Async Processing


!!! question "How to Scale Your Database?"

    ??? tip "Video"

        <iframe width="560" height="315" src="https://www.youtube.com/embed/_1IKwnbscQU?si=5gdpbjG31SPR1uP3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

        - Indexing
        - Materialized Views
        - Denormalization
        - Vertical Scaling
        - Horizontal Scaling
        - Database Caching
        - Replication
        - Sharding


!!! question "How to Improve API Performance?"

    ??? tip "Video"

        <iframe width="560" height="315" src="https://www.youtube.com/embed/zvWKqUiovAM?si=0JIYNvFGLvZD2cpC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

        - Caching
        - Pagination
        - Avoiding N+1 Queries
        - Asynchronous Processing
        - Connection Pooling
        - Payload Compression
        - JSON Serializers


!!! question "What is gRPC?"

    ??? tip "Answer"

        gRPC

        https://www.youtube.com/shorts/t0ONFCY6NWI


!!! question "Distributed System Design Patterns"

    ??? tip "Video"

        <iframe width="560" height="315" src="https://www.youtube.com/embed/nH4qjmP2KEE?si=8HI6aRVBxW5CtwOz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

        - Ambassador
        - Circuit Breaker
        - CQRS
        - Event Sourcing
        - Leader Election
        - Pub-Sub
        - Sharding

!!! question "What is OAuth 2.0?"

    ??? tip "Answer"

        OAuth 2.0 is an authorization framework that allows third-party applications to access a user's resources without exposing their credentials. It involves four main roles:
        
        - the resource owner (typically the user),
        - the client (the app that wants access),
        - the authorization server, and
        - the resource server.
        
        The user gives permission to the client through the authorization server, which then issues an access token. This token is then used by the client to access the user's resources on the resource server. It keeps everything secure and user credentials safe!