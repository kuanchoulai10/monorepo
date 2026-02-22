---
tags:
  - Python
  - Go
---

# Error Handling & Defer

Python's try/except mapped to Go's `if err != nil` pattern, and related error handling constructs.

## try / except

=== "Python"

    ```python
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Parse error: {e}")
    ```

=== "Go"

    ```go
    var data map[string]any
    err := json.Unmarshal([]byte(raw), &data)
    if err != nil {
        fmt.Printf("Parse error: %v\n", err)
    }
    ```

    !!! warning "Go has no exceptions"

        Errors are return values. Callers **must** check `err`. Ignoring errors is an anti-pattern in Go.

## raise

=== "Python"

    ```python
    def divide(a, b):
        if b == 0:
            raise ValueError("division by zero")
        return a / b
    ```

=== "Go"

    ```go
    func divide(a, b float64) (float64, error) {
        if b == 0 {
            return 0, fmt.Errorf("division by zero")
        }
        return a / b, nil
    }

    result, err := divide(10, 0)
    if err != nil {
        log.Fatal(err)
    }
    ```

## Multiple Exceptions

=== "Python"

    ```python
    try:
        result = do_something()
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission denied")
    except Exception as e:
        print(f"Other error: {e}")
    ```

=== "Go"

    ```go
    err := doSomething()
    if errors.Is(err, os.ErrNotExist) {
        fmt.Println("File not found")
    } else if errors.Is(err, os.ErrPermission) {
        fmt.Println("Permission denied")
    } else if err != nil {
        fmt.Printf("Other error: %v\n", err)
    }
    ```

## finally

=== "Python"

    ```python
    f = open("file.txt")
    try:
        data = f.read()
    finally:
        f.close()
    ```

=== "Go"

    ```go
    // "defer" ensures a function runs when the surrounding function returns
    f, err := os.Open("file.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()  // runs automatically when the function exits

    data, err := io.ReadAll(f)
    ```

    !!! warning "`defer` is LIFO (last in, first out)"

        Multiple `defer` calls execute in reverse order:

        ```go
        defer fmt.Println("first")
        defer fmt.Println("second")
        defer fmt.Println("third")
        // Output: third, second, first
        ```

## Context Manager

=== "Python"

    ```python
    with open("file.txt") as f:
        data = f.read()
    # f is automatically closed
    ```

=== "Go"

    ```go
    f, err := os.Open("file.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    data, err := io.ReadAll(f)
    ```

## Custom Exception

=== "Python"

    ```python
    class NotFoundError(Exception):
        def __init__(self, name: str):
            self.name = name
            super().__init__(f"{name} not found")

    raise NotFoundError("user")
    ```

=== "Go"

    ```go
    type NotFoundError struct {
        Name string
    }

    // Implement the error interface
    func (e *NotFoundError) Error() string {
        return fmt.Sprintf("%s not found", e.Name)
    }

    func findUser(name string) error {
        return &NotFoundError{Name: name}
    }

    // Use errors.As to extract the concrete error type
    var nfe *NotFoundError
    if errors.As(err, &nfe) {
        fmt.Printf("Missing: %s\n", nfe.Name)
    }
    ```

    !!! warning "`panic`/`recover` is not normal error handling"

        Go has `panic` and `recover`, but they are reserved for truly unrecoverable errors
        (e.g., programmer bugs). Normal error handling always uses `return error`.
