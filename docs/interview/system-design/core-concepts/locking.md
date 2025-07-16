# Locking

!!! question "What is a distributed lock and why do we need it?"

    ??? tip "Answer"

        A distributed lock is a mechanism used in distributed systems to ensure that only one process or thread can access a shared resource at a time. This is important for **preventing conflicts** and **ensuring data consistency**, especially when multiple processes are running on different machines. It's similar to how a traditional database lock works, but it's designed to work across multiple machines or services.

!!! question "Could you give an practical example of how it works?"

    ??? tip "Answer"

        Take an online ticketing platform like Ticketmaster. When a user selects a ticket and starts the checkout process, you need to temporarily lock that ticket — maybe for 10 minutes — so no one else can buy it during that time. A distributed lock helps enforce that across all servers in the system. 
        
        A common way to implement it is using a distributed key-value store like **Redis**. For example, let's say we want to lock a concert ticket with ID `abc`. We can store a key like `abc` in Redis with a value like **locked**. Since Redis operations are atomic, if another process tries to lock the same ticket, it'll fail because the key already exists. Once the first process is done with the lock, it can set the value of `abc` to `unlocked` and another process can acquire the lock.

        Another handy feature of distributed locks is that they can **be set to expire after a certain amount of time**. This is great for ensuring that locks **don't get stuck in a locked state if a process crashes or is killed**. For example, if you set the value of `abc` to `locked` and then the process crashes, the lock will expire after a certain amount of time (like 10 minutes) and another process can acquire the lock at that point.

!!! question "What are typical use cases for distributed locks?"

    ??? tip "Answer"

        Sure, there are several scenarios where distributed locks are really useful, especially in large-scale systems where consistency and coordination across services or nodes are critical.

        First, a common example is in **e-commerce checkout systems**. Let's say you're selling a limited-edition sneaker. When a user adds it to their cart and proceeds to checkout, you want to prevent others from buying the same item at the same time. So you might use a distributed lock to "hold" that item for the user for a short period — maybe 10 minutes — while they complete the payment process. This helps avoid overselling.

        Another case is in **ride-sharing or food delivery platforms**. When a rider or customer makes a request, the system needs to assign a nearby driver. Here, a distributed lock can help ensure that one driver isn’t accidentally assigned to multiple customers. The lock would be held while waiting for the driver to confirm or reject the assignment, or until a timeout.

        Lastly, in **online auction platforms**, distributed locks can be helpful during the final moments of bidding. For example, when a user places a bid at the last second, you want to briefly lock the auction item to ensure that only one bid is processed at a time. This avoids race conditions and ensures the integrity of the bidding process.

!!! question "What is deadlocks? How to prevent or deal with it?"

    ??? tip "Answer"
    
        Deadlocks can occur when two or more processes are waiting for each other to release a lock. Think about a situation where two processes are trying to acquire two locks at the same time. One process acquires lock A and then tries to acquire lock B, while the other process acquires lock B and then tries to acquire lock A. This can lead to a situation where both processes are waiting for each other to release a lock, causing a deadlock.

        To prevent them, you can use techniques like setting **timeouts** on your locks, so if a lock isn't released within a certain period, it just gets automatically released. Another approach is to **implement lock ordering, where you make sure that all processes acquire locks in a specific order to avoid circular waiting**.

!!! question "What is the difference between optimistic and pessimistic locking? What are the pros and cons of each approach, and when should each be used?"

    ??? tip "Answer"

        Optimistic and pessimistic locking are two strategies for managing resource consistency.

        With **optimistic locking**, the system assumes that **conflicts are rare**, so **it doesn't lock the data when a user starts a transaction**. Instead, it **checks for conflicts when the transaction is committed**. If there's a conflict, it will prompt the user to retry. **It's great when conflicts are infrequent** because **it reduces the overhead of locking resources** and is generally more efficient when conflicts are rare.

        On the other hand, **pessimistic locking** assumes that **conflicts are likely**, so it locks the data as soon as a transaction starts. This prevents other transactions from accessing the data until the lock is released. It's useful when **you expect a lot of contention**, but it can **cause delays and can reduce system performance if overused** especially if there are a lot of transactions happening at once.

        In terms of when to use each: optimistic locking is great for scenarios where you don't expect a lot of conflicts, and you want to keep things running smoothly and efficiently. Pessimistic locking is better when you know there will be a lot of contention and you need to ensure that no data corruption or inconsistency happens.


- [Locking | Hello Interview](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts#locking)
- [Distributed Lock | Hello Interview](https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies#distributed-lock)