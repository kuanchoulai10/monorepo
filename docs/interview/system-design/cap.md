# CAP

<iframe width="560" height="315" src="https://www.youtube.com/embed/BHqjEjzAicA?si=Ae8LeyBNjl71WD__" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/VdrEq0cODu4?si=1E7yrWKkQdjWlbuD" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

!!! question "What is CAP Theorem?"

    ??? tip "Answer"

        CAP theorem is a concept in distributed computing states that **a distributed data store can't simultaneously provide all three of the following guarantees: consistency, availability, and partition tolerance**. According to the theorem, **a system can only guarantee two out of these three at the same time**. It's a useful way to think about the trade-offs when choosing distributed systems.

        With the CAP theorem,

        - the first part is **consistency**, which means that every time you read data, you get the most up-to-date information, or you get an error if it can't provide that up-to-date information.
        - The second part is **availability**, which means that every request you make gets a response, even if it might not be the most up-to-date information.
        - And the third part is **partition tolerance**, which means that the system continues to work even if there are network issues that split the system into separate parts.

        Let's go through three examples, each focusing on a different pair of the CAP theorem guarantees.

        First, if we consider a system that prioritizes **consistency and availability (CA)**, it means that every read will get the latest write, and the system will always respond to requests. However, if there's a network partition, the system might have to sacrifice partition tolerance because it will need to ensure that all nodes are perfectly in sync before responding. These systems are often used in environments where **network partitions are either rare or not a big concern**. **A good example is a traditional relational database that runs on a single server or a cluster** that doesn't usually face network issues. **Banks or financial institutions** often prefer CA systems because they need consistent and available data, and they can control the environment to reduce network partitions.

        Second, if we look at a system that ensures **consistency and partition tolerance (CP)**, that means it will always give you the most up-to-date data, and it will continue to function even if there's a network partition. But it might sacrifice availability because it could refuse to respond if it can't guarantee that consistency. An example of this would be a **distributed database that uses strong consistency protocols, to ensure that most of the nodes agree on the data before responding, even if that means delaying responses**. This is often important in industries like **healthcare or finance**, where data accuracy is critical, and you want to ensure that all parts of the system reflect the same data, even if that means sacrificing a bit of availability.

        Lastly, if we focus on **availability and partition tolerance (AP)**, that means the system will always give a response and keep working even if there's a network partition, but it might not always give you the most up-to-date data. This is what we often see in **eventually consistent **systems, like some NoSQL databases. An example of this would be a **social media platform** where you can still post updates and read posts even if some parts of the system are temporarily out of sync. These systems are designed to handle high traffic and ensure that users can always interact with the platform, even if it means that some data might not be perfectly consistent across all nodes at all times.
