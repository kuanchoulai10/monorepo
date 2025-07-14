# Design a Rate Limiter

<iframe width="560" height="315" src="https://www.youtube.com/embed/dpEOhfEEoyw?si=JQrqZowv67zSI1-_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/SgWb6tWx3S8?si=1bpv6F1zIHVySY5x" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/VzW41m4USGs?si=RQLSy4FHTVo8LMea" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

!!! question "What is Rate Limiter?"

    ??? tip "Answer"

        A rate limiter is essentially a tool or mechanism that helps control the number of requests or actions that a user or system can make within a certain time frame. It's a way to prevent overloading a system with too many requests at once, which can help maintain performance and stability. It's super useful for things like APIs, where you want to make sure that no single user can overwhelm the service.

!!! question "What Are the Common Strategies for Rate Limiting? What Are the Pros and Cons of Each? When to Use Them?"

    ??? tip "Answer"

        There are a few common strategies for implementing rate limiting. 
        
        One popular approach is called **the token bucket algorithm**. **It allows a certain number of tokens to be added to a bucket at a fixed rate. Each request consumes a token, and once the tokens run out, further requests have to wait until new tokens are added**. The **pros** are that it's flexible and can handle short bursts of traffic really well, making it great for scenarios where you have unpredictable spikes. The **cons** are that it can be a bit complex to implement and fine-tune. It's best used **when** you want to allow bursts but still maintain a steady overall rate.

        Another approach is **the leaky bucket algorithm**, which **processes requests at a fixed rate, similar to water leaking out of a bucket. If requests come in too quickly, they get queued up and processed at that steady rate**. The **pros** here are that it smooths out traffic and prevents sudden spikes from overwhelming your system. The **cons** are that it can introduce some latency if there's a sudden influx of requests. This is best used **when** you want to maintain a consistent flow of requests and avoid sudden surges.
        
        There's also **the fixed window counter**, where **counts the number of requests in a fixed time window, and if the count exceeds a certain limit, further requests are blocked until the window resets**. The **pros** are that it's simple and easy to implement, and it's straightforward to understand. The **cons** are that it can lead to something called the "thundering herd" problem, where a lot of requests come in right at the start of a new window. This is best used **when** you want a straightforward approach and you're not too concerned about handling bursts more gracefully.

        Another common strategy is **the sliding window algorithm**. This method is a bit more dynamic than the fixed window because **it uses a rolling or sliding window of time to count requests**. This means that instead of resetting the count at the start of each fixed window, **it continuously adjusts, giving you a more accurate and smoother rate limiting experience**. The **pros** are that it reduces the burstiness that can happen at boundary points of fixed windows and provides a more even distribution of requests. The **cons** are that it can be a bit more complex to implement than the fixed window, but it's definitely worth it when you need that smoother rate limiting. It's great for **situations** where traffic patterns are more constant, and you want to avoid sudden spikes.

!!! question "What's your recommendation for getting started with implementing rate limiting?"

    ??? tip "Answer"

        A good starting point is to begin with **something simple and easy to understand**, like **the token bucket algorithm**. It's pretty flexible and works well for a variety of use cases. You can start by setting a reasonable limit based on your system's capacity and then adjust as you see how it affects your traffic. Once you're comfortable, you can experiment with other algorithms or even combine strategies to get the best of both worlds. It's all about iterating and fine-tuning as you go!


!!! question "Where should I implement rate-limiting logic — on the server side, client side, or in the middleware? What are your suggestions for each of these options?"

    ??? tip "Answer"

        You can actually implement rate limiting in all of those places, and each has its own advantages.
        
        On the **client** side, implementing rate limiting can help you **avoid sending too many requests in the first place**, which can reduce the load on the server and potentially save resources.
        
        **Middleware** is a great option because it sits between the client and the server, so it can **handle rate limiting for multiple clients in a centralized way**. This is often a sweet spot because **it's easy to manage and update without touching the client or server code directly**.
        
        On the **server** side, you **have the most control** because you can enforce limits directly where the resources are being consumed, but it can also **add a bit of complexity and overhead**.
        
        So, it really depends on your specific needs, but **middleware is often a nice balance between the two**!

!!! question "What are the pros and cons of limiting requests by user ID versus by IP address?"

    ??? tip "Answer"

        When you limit requests by **user ID**, it allows you to have **more granular control**, and it ensures that each individual user is treated fairly. This can be great for applications **where users have accounts and you want to prevent any one user from monopolizing resources**. The **downside** is that **you need a reliable way to identify users, which might not always be possible, especially if users don't have to log in**.

        On the other hand, limiting by **IP address** can be **easier to implement** because every request comes with an IP address, so you can **start rate limiting without requiring user authentication**. However, the **downside** is that **multiple users might share the same IP address**, like in an office or a household, which could lead to innocent users being rate limited. Plus, IP addresses can be spoofed or changed, so it might not always be as reliable as user identification.
        
        Ultimately, the best approach often depends on the nature of your application and your users.

!!! question "Which situations are best for each of these strategies (limiting by user ID or IP address), in your opinion?"

    ??? tip "Answer"

        If you have a **user-centric application** where users are authenticated and you can reliably identify them, then rate limiting by user ID is a great approach. It ensures fairness and prevents any single user from abusing the system.
        
        On the other hand, if you have an application where **users are mostly anonymous** or you don't have a reliable way to identify them, then IP-based rate limiting can still be effective. It’s a good starting point, even though it might not be perfect.
