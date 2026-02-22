---
tags:
  - Python
  - Go
---

# Primitive Types & Variables

Type declarations, conversions, zero values, and variable patterns.

## Variables

=== "Python"

    ```python
    x = 10              # type inferred
    name = "Alice"
    x, y = 1, 2         # multiple assignment
    a, b = b, a         # swap
    ```

=== "Go"

    ```go
    x := 10              // short declaration (type inferred)
    var x int = 10       // explicit type
    var name string      // zero value: ""

    x, y := 1, 2         // multiple assignment
    a, b = b, a          // swap
    ```

    !!! warning "`:=` vs `var`"

        `:=` can only be used inside functions. Package-level variables must use `var`.

## int / float

=== "Python"

    ```python
    x = 10
    y = 3.14
    z = x + y            # 13.14 (auto-promotes to float)

    7 / 2                 # 3.5  (true division)
    7 // 2                # 3    (floor division)
    ```

=== "Go"

    ```go
    var x int = 10
    var y float64 = 3.14
    z := float64(x) + y  // must convert explicitly

    7 / 2                 // 3   (integer division)
    float64(7) / 2        // 3.5
    ```

    !!! warning "No implicit numeric conversion"

        Go does not auto-promote types. Mixing `int` and `float64` in an expression is a compile error — you must convert explicitly.

## str

=== "Python"

    ```python
    name = "Alice"
    greeting = f"Hello, {name}!"       # f-string

    multi = """line one
    line two"""

    full = "Hello" + " " + "World"     # concatenation
    ```

=== "Go"

    ```go
    name := "Alice"
    greeting := fmt.Sprintf("Hello, %s!", name)  // fmt.Sprintf

    multi := `line one
    line two`                                     // raw string literal

    full := "Hello" + " " + "World"               // concatenation
    ```

## bool

=== "Python"

    ```python
    x = True
    y = False
    ```

=== "Go"

    ```go
    x := true
    y := false
    ```

    !!! warning "Capitalization matters"

        Python uses `True`/`False` (capitalized). Go uses `true`/`false` (lowercase).

## None

=== "Python"

    ```python
    x = None
    if x is None:
        print("no value")
    ```

=== "Go"

    ```go
    // Go has no universal "None". nil applies to specific types:
    var p *int            // nil pointer
    var m map[string]int  // nil map
    var s []int           // nil slice

    if p == nil {
        fmt.Println("no value")
    }
    ```

    !!! warning "Zero values"

        Go variables are initialized to their zero value automatically:
        `int` → `0`, `string` → `""`, `bool` → `false`, pointers/maps/slices → `nil`.

## Type Conversion

=== "Python"

    ```python
    int("42")         # 42
    str(42)           # "42"
    float("3.14")     # 3.14
    bool(0)           # False
    ```

=== "Go"

    ```go
    strconv.Atoi("42")              // 42, error
    strconv.Itoa(42)                // "42"
    strconv.ParseFloat("3.14", 64)  // 3.14, error

    // Type casting (numeric only)
    float64(42)                     // 42.0
    int(3.14)                       // 3
    ```

    !!! warning "String ↔ number requires `strconv`"

        `string(65)` does **not** give `"65"` — it gives `"A"` (the Unicode character). Use `strconv.Itoa` for number-to-string conversion.
