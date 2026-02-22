---
tags:
  - Python
  - Go
---

# Functions

Function definition, multiple return values, variadic, lambda, closures, and decorators.

## def

=== "Python"

    ```python
    def greet(name: str) -> str:
        return f"Hello, {name}"
    ```

=== "Go"

    ```go
    func greet(name string) string {
        return fmt.Sprintf("Hello, %s", name)
    }
    ```

## Multiple Return Values

=== "Python"

    ```python
    def divide(a, b):
        if b == 0:
            return 0, False
        return a / b, True

    result, ok = divide(10, 3)
    ```

=== "Go"

    ```go
    func divide(a, b float64) (float64, bool) {
        if b == 0 {
            return 0, false
        }
        return a / b, true
    }

    result, ok := divide(10, 3)
    ```

## *args

=== "Python"

    ```python
    def total(*nums):
        return sum(nums)

    total(1, 2, 3)          # 6
    total(*[1, 2, 3])       # unpack list
    ```

=== "Go"

    ```go
    func total(nums ...int) int {
        sum := 0
        for _, n := range nums {
            sum += n
        }
        return sum
    }

    total(1, 2, 3)           // 6
    total([]int{1, 2, 3}...) // unpack slice
    ```

## **kwargs

=== "Python"

    ```python
    def connect(host, port=5432, timeout=30, ssl=True):
        ...

    connect("localhost", port=3306, ssl=False)
    ```

=== "Go"

    ```go
    // Go has no keyword arguments — use an options struct instead
    type ConnectOpts struct {
        Port    int
        Timeout int
        SSL     bool
    }

    func connect(host string, opts ConnectOpts) {
        if opts.Port == 0 { opts.Port = 5432 }
        if opts.Timeout == 0 { opts.Timeout = 30 }
        // ...
    }

    connect("localhost", ConnectOpts{Port: 3306, SSL: false})
    ```

    !!! warning "Zero value trap with defaults"

        A struct field's zero value (`0`, `false`, `""`) is indistinguishable from "not set".
        If you need to tell them apart, use pointer fields (`*int`) or a separate bool flag.

## lambda

=== "Python"

    ```python
    double = lambda x: x * 2
    nums = [1, 2, 3]
    result = list(map(double, nums))   # [2, 4, 6]
    ```

=== "Go"

    ```go
    double := func(x int) int { return x * 2 }
    nums := []int{1, 2, 3}
    result := make([]int, len(nums))
    for i, n := range nums {
        result[i] = double(n)
    }
    ```

## Closure

=== "Python"

    ```python
    def make_counter():
        count = 0
        def increment():
            nonlocal count
            count += 1
            return count
        return increment

    counter = make_counter()
    counter()   # 1
    counter()   # 2
    ```

=== "Go"

    ```go
    func makeCounter() func() int {
        count := 0
        return func() int {
            count++
            return count
        }
    }

    counter := makeCounter()
    counter()   // 1
    counter()   // 2
    ```

## Decorator

=== "Python"

    ```python
    import time

    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print(f"Took {time.time() - start:.2f}s")
            return result
        return wrapper

    @timer
    def slow_func():
        time.sleep(1)
    ```

=== "Go"

    ```go
    // Go has no decorator syntax — use a wrapper function instead
    func timer(fn func()) func() {
        return func() {
            start := time.Now()
            fn()
            fmt.Printf("Took %v\n", time.Since(start))
        }
    }

    slowFunc := timer(func() {
        time.Sleep(1 * time.Second)
    })
    slowFunc()
    ```
