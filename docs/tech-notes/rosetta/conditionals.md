---
tags:
  - Python
  - Go
---

# Conditionals

if/else, ternary expressions, match/case, and truthy/falsy rules.

## if / elif / else

=== "Python"

    ```python
    score = 85

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"
    ```

=== "Go"

    ```go
    score := 85

    if score >= 90 {
        grade = "A"
    } else if score >= 80 {
        grade = "B"
    } else {
        grade = "C"
    }
    ```

    !!! warning "No parentheses, braces are required"

        Go does not use parentheses around conditions, but braces `{}` are mandatory — even for single-line bodies.

## Ternary

=== "Python"

    ```python
    status = "even" if x % 2 == 0 else "odd"
    ```

=== "Go"

    ```go
    // Go has no ternary operator — use a full if/else
    var status string
    if x%2 == 0 {
        status = "even"
    } else {
        status = "odd"
    }
    ```

## match / case

=== "Python"

    ```python
    # Python 3.10+ structural pattern matching
    match command:
        case "quit":
            sys.exit()
        case "hello" | "hi":
            print("Hello!")
        case str(s) if s.startswith("/"):
            print(f"Command: {s}")
        case _:
            print("Unknown")
    ```

=== "Go"

    ```go
    switch command {
    case "quit":
        os.Exit(0)
    case "hello", "hi":
        fmt.Println("Hello!")
    default:
        if strings.HasPrefix(command, "/") {
            fmt.Printf("Command: %s\n", command)
        } else {
            fmt.Println("Unknown")
        }
    }
    ```

    !!! warning "Go `switch` does not fall through by default"

        Unlike C/Java, Go's `switch` breaks automatically after each case.
        Use `fallthrough` explicitly if needed.

## Truthy / Falsy

=== "Python"

    ```python
    # These are all falsy:
    bool(None)      # False
    bool(0)         # False
    bool("")        # False
    bool([])        # False
    bool({})        # False

    if my_list:     # truthy check — non-empty list is True
        process(my_list)
    ```

=== "Go"

    ```go
    // Go requires explicit bool — no truthy/falsy
    if len(myList) > 0 {      // must compare explicitly
        process(myList)
    }

    if name != "" {           // cannot just use: if name {
        fmt.Println(name)
    }
    ```

    !!! warning "Go conditions must be `bool`"

        You cannot use `if x {` where `x` is an int, string, or pointer. Go requires an explicit boolean expression.
