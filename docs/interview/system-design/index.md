# System Design Questions

## Schedule

| Date          | Candidate | Question                                                                         |
| ------------- | --------- | -------------------------------------------------------------------------------- |
| Jul. 23, 2025 | KC        | [Design FB Post Search](./infra/social-media-post-search/index.md)         |
| Jul. 22, 2025 | KC        | [Design Dropbox](./product/dropbox/index.md)                           |
| Jul. 16, 2025 | KC        | [Design a Top K Heavy Hitters Service](./infra/top-k-heavy-hitters/index.md)     |
| Jul. 15, 2025 | KC        | [✅ Design Ticketmaster](./product/ticket-booking-site/index.md)                      |
| Jul. 12, 2025 | KC        | [✅ Design a Distributed Message Queue](./infra/distributed-message-queue/index.md) |
| Jyl.  9, 2025 | KC        | [✅ Design Uber](./product/ride-sharing-service/index.md)                             |

## Core Concepts

- [x] [CAP Theorem](./core-concepts/cap/index.md)
- [x] [Consistent Hashing](./core-concepts/consistent-hashing/index.md)
- [ ] [Indexing](./core-concepts/indexing/index.md)
- [ ] [Locking](./core-concepts/locking/index.md)
- [ ] [Consensus Algorithms](./core-concepts/consensus-algorithms/index.md)
- [ ] [API Performance Optimization](./core-concepts/api-perf-opt/index.md)
- [ ] [Database Performance Optimization](./core-concepts/db-perf-opt/index.md)
- [ ] [Scale From Zero To Millions Of Users](https://bytebytego.com/courses/system-design-interview/scale-from-zero-to-millions-of-users)
- [ ] [Back-of-the-envelope Estimation](https://bytebytego.com/courses/system-design-interview/back-of-the-envelope-estimation)

## Key Technologies

- [x] [Kafka](./key-technologies/kafka/index.md)
- [x] [Spark](./key-technologies/spark/index.md)
- [ ] [Flink](./key-technologies/flink/index.md)
- [ ] [DynamoDB](./key-technologies/dynamodb/index.md)
- [ ] [Elasticsearch](./key-technologies/elasticsearch/index.md)
- [ ] [Redis](./key-technologies/redis/index.md)

## Product

In these interviews, you'll be asked to design a system behind a product.

- [x] [Design a Ride-Sharing Service Like Uber](./product/ride-sharing-service/index.md)
- [x] [Design a Ticket Booking Site Like Ticketmaster](./product/ticket-booking-site/index.md)
- [ ] [Design a Messaging Service Like WhatsApp](./product/messaging-service/index.md)

## Infrastructure

In these interviews, you'll be asked to design a system that supports a particular infrastructure use case.

- [x] [Design a Distributed Message Queue](./infra/distributed-message-queue/index.md)
- [ ] [Design a Top K Heavy Hitters Service](./infra/top-k-heavy-hitters/index.md)
- [ ] [Design a Rate Limiter](./infra/rate-limiter/index.md)
- [ ] [Design a Notification Service](./infra/notification-service/index.md)
- [ ] [Design a Key-Value Store](./infra/key-value-store/index.md)

## Machine Learning

In these interviews, you'll be asked to design a system that supports a particular machine learning use case.

- [ ] [Design an Instagram Ranking Model](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/design-instagram-feed-ranking-model)
- [ ] [Deploy and Monitor an Instagram Ranking Model](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/deploy-and-monitor-instagram-feed-ranking-model)
- [ ] [Design a Spotify Recommendation System](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/design-spotify-recommendation-system)
- [ ] [Design Evaluation Framework for Ads Ranking System](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/design-evaluation-framework-for-ads-ranking)
- [ ] [Design a System to Predict Netflix Watch Times](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/model-predict-netflix-watch-times)
- [ ] [Train a Model to Detect Bots](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/train-model-detect-bots)
- [ ] [Design a Landmark Recognition System](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/landmark-recognition)
- [ ] [Design a System to Predict Youtube Ad Conversions](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/design-system-predict-youtube-ad-conversions)
- [ ] [Design an ETA System for a Maps App](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/design-eta-system-maps-app)
- [ ] [Design an App Suggestion System for Phones](https://www.tryexponent.com/courses/ml-engineer/ml-system-design/app-suggestion-system)

## Data Pipeline

In these interviews, you'll be asked to design a system that supports a particular data pipeline use case.

- [ ] [Create a Data Pipeline for Netflix Clickstream Data](https://www.youtube.com/watch?v=YRTIpSuiFh8)
- [ ] [Design an ETL Process for Student Interaction](https://www.youtube.com/watch?v=LEAlAC8KMLU)
- [ ] [Design an ETL Pipeline for a ML Platform for AWS](https://www.youtube.com/watch?v=eAjMNExUXdk)

## Data Modeling

In these interviews, you'll be asked to design a data model for a particular use case.

- [ ] [Design a Data Warehouse Schema for a Ride-Sharing Service](https://www.tryexponent.com/courses/data-engineering/data-modeling-interviews/ride-sharing-data-model)
- [ ] [Design a Data Warehouse Schema for Customer Support](https://www.tryexponent.com/courses/data-engineering/data-modeling-interviews/customer-support-data-model)
- [ ] [Design a Data Warehouse Schema for Airbnb](https://www.tryexponent.com/courses/data-engineering/data-modeling-interviews/airbnb-data-model)
- [ ] [Design a Data Warehouse Schema for Stripe](https://www.tryexponent.com/courses/data-engineering/data-modeling-interviews/stripe-data-model)
- [ ] [Design a Data Warehouse Schema for Instagram](https://www.tryexponent.com/courses/data-engineering/data-modeling-interviews/instagram-data-model)


## Data Architecture

In these interviews, you'll be asked to design a data architecture for a particular use case.


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