---
tags:
  - Python
  - Go
---

# Loops & Iteration

for, while, enumerate, zip, range — and their equivalents.

## for ... in

=== "Python"

    ```python
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(fruit)
    ```

=== "Go"

    ```go
    fruits := []string{"apple", "banana", "cherry"}
    for _, fruit := range fruits {
        fmt.Println(fruit)
    }
    ```

## enumerate

=== "Python"

    ```python
    fruits = ["apple", "banana", "cherry"]
    for i, fruit in enumerate(fruits):
        print(f"{i}: {fruit}")
    ```

=== "Go"

    ```go
    fruits := []string{"apple", "banana", "cherry"}
    for i, fruit := range fruits {
        fmt.Printf("%d: %s\n", i, fruit)
    }
    ```

## dict.items()

=== "Python"

    ```python
    scores = {"alice": 90, "bob": 85}
    for name, score in scores.items():
        print(f"{name}: {score}")
    ```

=== "Go"

    ```go
    scores := map[string]int{"alice": 90, "bob": 85}
    for name, score := range scores {
        fmt.Printf("%s: %d\n", name, score)
    }
    ```

## while

=== "Python"

    ```python
    n = 10
    while n > 0:
        n -= 1
    ```

=== "Go"

    ```go
    // Go has no "while" keyword — use "for" with a condition
    n := 10
    for n > 0 {
        n--
    }
    ```

## while True

=== "Python"

    ```python
    while True:
        line = input()
        if line == "quit":
            break
    ```

=== "Go"

    ```go
    scanner := bufio.NewScanner(os.Stdin)
    for {
        scanner.Scan()
        if scanner.Text() == "quit" {
            break
        }
    }
    ```

## range

=== "Python"

    ```python
    for i in range(5):          # 0, 1, 2, 3, 4
        print(i)

    for i in range(2, 8, 2):   # 2, 4, 6
        print(i)
    ```

=== "Go"

    ```go
    for i := range 5 {          // 0, 1, 2, 3, 4 (Go 1.22+)
        fmt.Println(i)
    }

    for i := 2; i < 8; i += 2 { // 2, 4, 6
        fmt.Println(i)
    }
    ```

## zip

=== "Python"

    ```python
    names = ["alice", "bob"]
    scores = [90, 85]
    for name, score in zip(names, scores):
        print(f"{name}: {score}")
    ```

=== "Go"

    ```go
    // Go has no built-in zip — use an index loop instead
    names := []string{"alice", "bob"}
    scores := []int{90, 85}
    for i := 0; i < len(names) && i < len(scores); i++ {
        fmt.Printf("%s: %d\n", names[i], scores[i])
    }
    ```

    !!! warning "`range` copies the value"

        `for _, v := range slice` gives you a copy of each element. Modifying `v` does not
        affect the original slice. Use the index to modify in place:

        ```go
        for i := range items {
            items[i].Count++  // modifies the original element
        }
        ```
