---
tags:
  - Python
  - Go
---

# Collections

Common operations on Python's list, dict, set, and string, and their equivalents in other languages.

## List

### Create

=== "Python"

    ```python
    numbers = [1, 2, 3, 4]
    empty = []
    ```

=== "Go"

    ```go
    numbers := []int{1, 2, 3, 4}
    empty := []int{}
    ```

### append / extend

=== "Python"

    ```python
    lst = [1, 2]
    lst.append(3)        # [1, 2, 3]
    lst.extend([4, 5])   # [1, 2, 3, 4, 5]
    ```

=== "Go"

    ```go
    lst := []int{1, 2}
    lst = append(lst, 3)        // [1, 2, 3]
    lst = append(lst, 4, 5)     // [1, 2, 3, 4, 5]
    ```

    !!! warning "`append` must capture the return value"

        Go's `append` does not modify the original slice. You must reassign:
        `lst = append(lst, ...)`. The underlying array may be reallocated if capacity is exceeded.

### pop / delete

=== "Python"

    ```python
    lst = [1, 2, 3, 4]
    last = lst.pop()      # last=4, lst=[1,2,3]
    del lst[0]            # lst=[2,3]
    ```

=== "Go"

    ```go
    lst := []int{1, 2, 3, 4}
    last := lst[len(lst)-1]                  // last=4
    lst = lst[:len(lst)-1]                   // [1,2,3]
    lst = append(lst[:0], lst[1:]...)        // [2,3]
    ```

### len / in

=== "Python"

    ```python
    lst = [1, 2, 3]
    len(lst)          # 3
    2 in lst          # True
    ```

=== "Go"

    ```go
    lst := []int{1, 2, 3}
    len(lst)          // 3

    // No built-in "in" — use a loop
    found := false
    for _, v := range lst {
        if v == 2 { found = true; break }
    }
    // Or use slices.Contains (Go 1.21+)
    slices.Contains(lst, 2)
    ```

### Slicing

=== "Python"

    ```python
    lst = [0, 1, 2, 3, 4]
    lst[1:3]     # [1, 2]
    lst[:3]      # [0, 1, 2]
    lst[2:]      # [2, 3, 4]
    ```

=== "Go"

    ```go
    lst := []int{0, 1, 2, 3, 4}
    lst[1:3]     // [1, 2]
    lst[:3]      // [0, 1, 2]
    lst[2:]      // [2, 3, 4]
    ```

### Negative Indexing

=== "Python"

    ```python
    lst = [0, 1, 2, 3, 4]
    lst[-1]      # 4
    lst[-2:]     # [3, 4]
    ```

=== "Go"

    ```go
    lst := []int{0, 1, 2, 3, 4}
    lst[len(lst)-1]      // 4
    lst[len(lst)-2:]     // [3, 4]
    ```

    !!! warning "Go does not support negative indexing"

        You must manually compute the index with `len(s)-n`.

### Reverse

=== "Python"

    ```python
    lst = [1, 2, 3]
    reversed_lst = lst[::-1]       # [3, 2, 1]
    ```

=== "Go"

    ```go
    lst := []int{1, 2, 3}
    slices.Reverse(lst)            // [3, 2, 1] (Go 1.21+)
    ```

### List Comprehension

=== "Python"

    ```python
    nums = [1, 2, 3, 4, 5]
    doubled = [x * 2 for x in nums]           # [2, 4, 6, 8, 10]
    evens = [x for x in nums if x % 2 == 0]   # [2, 4]
    ```

=== "Go"

    ```go
    nums := []int{1, 2, 3, 4, 5}

    doubled := make([]int, 0, len(nums))
    for _, x := range nums {
        doubled = append(doubled, x*2)
    }

    evens := make([]int, 0)
    for _, x := range nums {
        if x%2 == 0 {
            evens = append(evens, x)
        }
    }
    ```

### filter / map

=== "Python"

    ```python
    nums = [1, 2, 3, 4, 5]
    result = list(map(lambda x: x**2, filter(lambda x: x > 2, nums)))
    # [9, 16, 25]
    ```

=== "Go"

    ```go
    nums := []int{1, 2, 3, 4, 5}
    var result []int
    for _, x := range nums {
        if x > 2 {
            result = append(result, x*x)
        }
    }
    // [9, 16, 25]
    ```

### sorted / list.sort

=== "Python"

    ```python
    nums = [3, 1, 4, 1, 5]
    sorted_nums = sorted(nums)     # returns new list
    nums.sort()                    # in-place

    # custom sort
    words = ["banana", "apple", "cherry"]
    words.sort(key=len)
    ```

=== "Go"

    ```go
    nums := []int{3, 1, 4, 1, 5}
    sorted := slices.Sorted(slices.Values(nums))  // returns new slice (Go 1.23+)
    slices.Sort(nums)                              // in-place

    // custom sort
    words := []string{"banana", "apple", "cherry"}
    sort.Slice(words, func(i, j int) bool {
        return len(words[i]) < len(words[j])
    })
    ```

## Dict

### Create

=== "Python"

    ```python
    user = {"name": "Alice", "age": 30}
    empty = {}
    ```

=== "Go"

    ```go
    user := map[string]any{"name": "Alice", "age": 30}
    empty := map[string]int{}
    // or use make
    empty2 := make(map[string]int)
    ```

    !!! warning "Writing to a nil map panics"

        ```go
        var m map[string]int  // nil map
        _ = m["key"]          // OK — returns zero value
        m["key"] = 1          // panic!
        ```
        Always initialize maps with `make()` or a literal `{}` before writing.

### get / check / delete

=== "Python"

    ```python
    user = {"name": "Alice", "age": 30}

    age = user.get("age", 0)   # get with default

    if "name" in user:         # check key exists
        print(user["name"])

    del user["age"]            # delete key
    ```

=== "Go"

    ```go
    user := map[string]any{"name": "Alice", "age": 30}

    age, ok := user["age"]     // comma-ok pattern
    if !ok {
        age = 0
    }

    if name, ok := user["name"]; ok {  // check key exists
        fmt.Println(name)
    }

    delete(user, "age")        // delete key
    ```

### Iterate

=== "Python"

    ```python
    for key, value in user.items():
        print(f"{key}: {value}")
    ```

=== "Go"

    ```go
    for key, value := range user {
        fmt.Printf("%s: %v\n", key, value)
    }
    ```

    !!! warning "Map iteration order is random"

        Go's map `range` order may differ on every run. If you need a consistent order, sort the keys first.

### Dict Comprehension

=== "Python"

    ```python
    names = ["alice", "bob"]
    name_len = {name: len(name) for name in names}
    # {"alice": 5, "bob": 3}
    ```

=== "Go"

    ```go
    names := []string{"alice", "bob"}
    nameLen := make(map[string]int)
    for _, name := range names {
        nameLen[name] = len(name)
    }
    ```

## Set

### Create, Add & Remove

Go has no built-in set. The common pattern is `map[T]bool` or `map[T]struct{}`.

=== "Python"

    ```python
    s = {1, 2, 3}
    s.add(4)
    s.discard(2)
    ```

=== "Go"

    ```go
    s := map[int]bool{1: true, 2: true, 3: true}
    s[4] = true    // add
    delete(s, 2)   // discard
    ```

### Union & Intersection

=== "Python"

    ```python
    a, b = {1, 2, 3}, {2, 3, 4}
    union = a | b            # {1, 2, 3, 4}
    inter = a & b            # {2, 3}
    ```

=== "Go"

    ```go
    a := map[int]bool{1: true, 2: true, 3: true}
    b := map[int]bool{2: true, 3: true, 4: true}

    // union
    union := make(map[int]bool)
    for k := range a { union[k] = true }
    for k := range b { union[k] = true }

    // intersection
    inter := make(map[int]bool)
    for k := range a {
        if b[k] { inter[k] = true }
    }
    ```

## String

### Reverse

=== "Python"

    ```python
    s = "hello"
    reversed_s = s[::-1]           # "olleh"
    ```

=== "Go"

    ```go
    s := "hello"
    runes := []rune(s)
    slices.Reverse(runes)
    reversed := string(runes)     // "olleh"
    ```

    !!! warning "Use `[]rune` when reversing strings"

        Go strings are byte slices. Reversing bytes directly will corrupt
        multi-byte characters (e.g., CJK characters). Always convert to `[]rune` first.
