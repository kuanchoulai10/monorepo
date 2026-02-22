---
tags:
  - Python
  - Go
---

# Language Overview

A high-level comparison of Python and Go — how they differ in philosophy, tooling, and runtime behavior.

| Aspect | Python | Go |
|--------|--------|-----|
| **Type system** | Dynamically typed | Statically typed |
| **Execution** | Interpreted (bytecode on CPython) | Compiled to native binary |
| **Formatting** | PEP 8 (convention) | `gofmt` (enforced) |
| **Package manager** | pip / PyPI | Go Modules |
| **Entry point** | Any script can run directly | `func main()` in `package main` |
| **Concurrency** | GIL limits true parallelism; use multiprocessing or asyncio | Goroutines + channels (true parallelism) |
| **Error handling** | Exceptions (`try`/`except`) | Explicit return values (`if err != nil`) |
| **OOP** | Class-based inheritance | Struct + interface (composition) |
| **Null** | `None` (single value) | `nil` (typed; applies to pointers, maps, slices, channels, interfaces) |
| **Generics** | Duck typing / type hints | Generics since Go 1.18 |
| **Unused variables** | Allowed | Compile error |
| **Semicolons** | Not required | Auto-inserted by compiler |
