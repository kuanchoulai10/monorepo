---
tags:
  - Python
  - Go
---

# Concurrency

Go's goroutines and channels are core language features, compared to Python's threading and asyncio.

## threading.Thread

=== "Python"

    ```python
    import threading

    def worker(name):
        print(f"Hello from {name}")

    t = threading.Thread(target=worker, args=("thread-1",))
    t.start()
    t.join()
    ```

=== "Go"

    ```go
    func worker(name string) {
        fmt.Printf("Hello from %s\n", name)
    }

    go worker("goroutine-1")
    time.Sleep(time.Second)  // simple wait (not production-ready)
    ```

    !!! warning "When `main` exits, all goroutines are killed"

        When the main function returns, all goroutines are terminated immediately — they
        won't finish. Use `sync.WaitGroup` or channels to wait properly.

## queue.Queue

Channels are typed pipes for communication between goroutines.

=== "Python"

    ```python
    import queue
    import threading

    q = queue.Queue()

    def producer():
        for i in range(3):
            q.put(i)

    def consumer():
        while True:
            item = q.get()
            print(f"Got: {item}")
            q.task_done()

    threading.Thread(target=producer).start()
    threading.Thread(target=consumer, daemon=True).start()
    q.join()
    ```

=== "Go"

    ```go
    ch := make(chan int)

    // Producer
    go func() {
        for i := range 3 {
            ch <- i
        }
        close(ch)
    }()

    // Consumer
    for item := range ch {
        fmt.Printf("Got: %d\n", item)
    }
    ```

    !!! warning "Unbuffered channels block"

        `make(chan int)` creates an unbuffered channel — the sender blocks until a receiver
        is ready. Use `make(chan int, 10)` for a buffered channel that can queue values.

## threading.Lock

=== "Python"

    ```python
    import threading

    lock = threading.Lock()
    counter = 0

    def increment():
        global counter
        with lock:
            counter += 1
    ```

=== "Go"

    ```go
    var (
        mu      sync.Mutex
        counter int
    )

    func increment() {
        mu.Lock()
        counter++
        mu.Unlock()
    }
    ```

## asyncio

=== "Python"

    ```python
    import asyncio

    async def fetch(url):
        await asyncio.sleep(1)  # simulate I/O
        return f"data from {url}"

    async def main():
        results = await asyncio.gather(
            fetch("url1"),
            fetch("url2"),
        )
        print(results)

    asyncio.run(main())
    ```

=== "Go"

    ```go
    func fetch(url string, ch chan<- string) {
        time.Sleep(1 * time.Second)
        ch <- fmt.Sprintf("data from %s", url)
    }

    func main() {
        ch := make(chan string, 2)
        go fetch("url1", ch)
        go fetch("url2", ch)

        for range 2 {
            fmt.Println(<-ch)
        }
    }
    ```

## ThreadPoolExecutor

=== "Python"

    ```python
    from concurrent.futures import ThreadPoolExecutor

    def process(item):
        return item * 2

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(process, [1, 2, 3, 4]))
    ```

=== "Go"

    ```go
    var wg sync.WaitGroup
    items := []int{1, 2, 3, 4}
    results := make([]int, len(items))

    for i, item := range items {
        wg.Add(1)
        go func() {
            defer wg.Done()
            results[i] = item * 2
        }()
    }
    wg.Wait()
    ```

## select (Go-specific)

`select` listens on multiple channels simultaneously, executing whichever case is ready first.

=== "Python"

    ```python
    # No direct equivalent in Python
    # The closest is asyncio.wait with FIRST_COMPLETED
    done, _ = await asyncio.wait(
        [task1, task2],
        return_when=asyncio.FIRST_COMPLETED,
    )
    ```

=== "Go"

    ```go
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() { time.Sleep(1 * time.Second); ch1 <- "one" }()
    go func() { time.Sleep(2 * time.Second); ch2 <- "two" }()

    select {
    case msg := <-ch1:
        fmt.Println("Received from ch1:", msg)
    case msg := <-ch2:
        fmt.Println("Received from ch2:", msg)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout")
    }
    ```

## Buffered vs Unbuffered Channel (Go-specific)

=== "Python"

    ```python
    # queue.Queue is unbounded by default
    q = queue.Queue()           # unbounded
    q = queue.Queue(maxsize=5)  # bounded
    ```

=== "Go"

    ```go
    unbuf := make(chan int)      // unbuffered: send blocks until received
    buf := make(chan int, 5)     // buffered: can queue up to 5 values

    // send does not block until the buffer is full
    buf <- 1
    buf <- 2
    fmt.Println(<-buf)  // 1
    ```

    !!! warning "Avoid goroutine leaks"

        A goroutine waiting on a channel that never receives data will never terminate (leak).
        Use `context.WithCancel` or `context.WithTimeout` to make goroutines cancellable:

        ```go
        ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()

        select {
        case result := <-ch:
            fmt.Println(result)
        case <-ctx.Done():
            fmt.Println("Cancelled")
        }
        ```
