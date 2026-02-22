---
tags:
  - Python
  - Go
---

# Structs, Methods & Interfaces

Python's class maps to Go's struct + methods + interfaces. Go has no inheritance — it uses composition instead.

## Class Definition

=== "Python"

    ```python
    class User:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def greet(self) -> str:
            return f"Hi, I'm {self.name}"
    ```

=== "Go"

    ```go
    type User struct {
        Name string
        Age  int
    }

    func (u User) Greet() string {
        return fmt.Sprintf("Hi, I'm %s", u.Name)
    }
    ```

## Constructor

=== "Python"

    ```python
    user = User("Alice", 30)
    ```

=== "Go"

    ```go
    // Go has no __init__ — use a NewXxx() function by convention
    func NewUser(name string, age int) *User {
        return &User{Name: name, Age: age}
    }

    user := NewUser("Alice", 30)
    ```

## Instance Method

=== "Python"

    ```python
    class Counter:
        def __init__(self):
            self.count = 0

        def increment(self):
            self.count += 1
    ```

=== "Go"

    ```go
    type Counter struct {
        count int
    }

    // Pointer receiver: can modify the struct's fields
    func (c *Counter) Increment() {
        c.count++
    }
    ```

    !!! warning "Value receiver vs Pointer receiver"

        A value receiver `func (c Counter)` operates on a copy — modifications won't
        be reflected on the original struct. Use a pointer receiver `func (c *Counter)`
        when you need to mutate state.

## classmethod / staticmethod

=== "Python"

    ```python
    class User:
        @classmethod
        def from_dict(cls, data: dict) -> "User":
            return cls(data["name"], data["age"])

        @staticmethod
        def validate_age(age: int) -> bool:
            return 0 < age < 150
    ```

=== "Go"

    ```go
    // Go has no class/static methods — use package-level functions
    func UserFromMap(data map[string]any) *User {
        return &User{
            Name: data["name"].(string),
            Age:  data["age"].(int),
        }
    }

    func ValidateAge(age int) bool {
        return age > 0 && age < 150
    }
    ```

## Private / Public

=== "Python"

    ```python
    class Account:
        def __init__(self, owner: str, balance: float):
            self.owner = owner         # public
            self._balance = balance    # convention: private
            self.__secret = "xxx"      # name mangling

        def get_balance(self) -> float:
            return self._balance
    ```

=== "Go"

    ```go
    type Account struct {
        Owner   string   // Uppercase = exported (public)
        balance float64  // lowercase = unexported (private)
    }

    func (a Account) Balance() float64 {
        return a.balance
    }
    ```

    !!! warning "Capitalization determines visibility"

        Go has one simple rule: **Uppercase = exported** (accessible from other packages),
        **lowercase = unexported**. This applies to struct fields, methods, functions,
        variables, and constants.

## ABC / Abstract

=== "Python"

    ```python
    from abc import ABC, abstractmethod

    class Shape(ABC):
        @abstractmethod
        def area(self) -> float:
            ...

    class Circle(Shape):
        def __init__(self, radius: float):
            self.radius = radius

        def area(self) -> float:
            return 3.14159 * self.radius ** 2
    ```

=== "Go"

    ```go
    type Shape interface {
        Area() float64
    }

    type Circle struct {
        Radius float64
    }

    // Circle automatically satisfies the Shape interface
    func (c Circle) Area() float64 {
        return 3.14159 * c.Radius * c.Radius
    }
    ```

    !!! warning "Interfaces are implicit"

        Go does not require `implements Shape`. As long as a struct implements all methods
        of an interface, it automatically satisfies it. This is called **structural typing**.

## Inheritance

=== "Python"

    ```python
    class Animal:
        def __init__(self, name: str):
            self.name = name

        def speak(self) -> str:
            return "..."

    class Dog(Animal):
        def speak(self) -> str:
            return f"{self.name} says Woof!"
    ```

=== "Go"

    ```go
    // Go has no inheritance — use struct embedding (composition)
    type Animal struct {
        Name string
    }

    func (a Animal) Speak() string {
        return "..."
    }

    type Dog struct {
        Animal  // embedding: Dog gets Animal's fields and methods
    }

    // Override Speak
    func (d Dog) Speak() string {
        return fmt.Sprintf("%s says Woof!", d.Name)
    }

    dog := Dog{Animal{Name: "Rex"}}
    dog.Name      // access embedded field directly
    dog.Speak()   // "Rex says Woof!"
    ```
