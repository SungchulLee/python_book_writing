# Custom Exceptions

Python allows creating custom exception classes by subclassing the built-in `Exception` class. Custom exceptions improve code clarity and enable specific error handling.

!!! tip "Mental Model"
    A custom exception is just a class that inherits from `Exception`. It gives a meaningful name to a specific failure condition so callers can catch it precisely. Start with a bare subclass (`class MyError(Exception): pass`) and add attributes only when the handler needs structured data about what went wrong.

## Basic Custom Exception

Create a custom exception by inheriting from `Exception`.

```python
class TooHotError(Exception):
    pass

def check_temperature(temp):
    if temp > 60:
        raise TooHotError
    print("Temperature is fine.")

try:
    check_temperature(65)
except TooHotError:
    print("Too hot!")
```

Output:
```
Too hot!
```


## Custom Exception with Message

Pass a message to provide context about the error.

```python
class TooHotError(Exception):
    pass

def check_temperature(temp):
    if temp > 60:
        raise TooHotError("Temperature exceeds safe limit.")
    print("Temperature is fine.")

try:
    check_temperature(65)
except TooHotError as e:
    print(e)
```

Output:
```
Temperature exceeds safe limit.
```


## Custom Exception with __init__

Override `__init__` for custom initialization.

```python
class TooHotError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg

raise TooHotError("Too hot for a walk.")
```


## Using super().__init__

The preferred approach uses `super()` to initialize the parent class.

```python
class TooHotError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

try:
    raise TooHotError("Temperature is 65°F, too hot!")
except TooHotError as e:
    print(e)
```

Output:
```
Temperature is 65°F, too hot!
```


## Practical Example

A class that raises custom exceptions based on conditions.

```python
class TooHotError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Walk:
    def __init__(self, temperature):
        self.temperature = temperature
    
    def walk(self):
        if self.temperature > 60:
            raise TooHotError("Too hot for a walk.")
        print("Enjoy walking!")

aug_7_2023 = Walk(65)

try:
    aug_7_2023.walk()
except TooHotError as e:
    print(e)
```

Output:
```
Too hot for a walk.
```


## When to Create Custom Exceptions

Create custom exceptions when:

- Built-in exceptions don't describe the error adequately
- You need to catch specific errors in your application
- You want to provide domain-specific error messages
- You need to add custom attributes to the exception

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw ${amount}. Balance is ${balance}."
        )
```


## Exception Hierarchy for Custom Classes

Create a hierarchy of related exceptions.

```python
class WeatherError(Exception):
    """Base class for weather-related errors."""
    pass

class TooHotError(WeatherError):
    pass

class TooColdError(WeatherError):
    pass

# Catch all weather errors
try:
    raise TooHotError("Heat wave!")
except WeatherError as e:
    print(f"Weather issue: {e}")
```

---

## Exercises


**Exercise 1.**
Create a custom exception hierarchy for a banking application: `BankError` (base), `InsufficientFundsError`, and `AccountNotFoundError`. Each should accept a meaningful message.

??? success "Solution to Exercise 1"

        ```python
        class BankError(Exception):
            pass

        class InsufficientFundsError(BankError):
            def __init__(self, balance, amount):
                self.balance = balance
                self.amount = amount
                super().__init__(
                    f"Cannot withdraw ${amount}: only ${balance} available"
                )

        class AccountNotFoundError(BankError):
            def __init__(self, account_id):
                self.account_id = account_id
                super().__init__(f"Account {account_id} not found")
        ```

    Custom exceptions inherit from a common base class, enabling both specific and broad catching.

---

**Exercise 2.**
Write a class `BankAccount` with methods `deposit(amount)` and `withdraw(amount)`. The `withdraw` method should raise `InsufficientFundsError` (from Exercise 1) if the balance would go negative. Include the current balance and requested amount in the error message.

??? success "Solution to Exercise 2"

        ```python
        class BankAccount:
            def __init__(self, balance=0):
                self.balance = balance

            def deposit(self, amount):
                self.balance += amount

            def withdraw(self, amount):
                if amount > self.balance:
                    raise InsufficientFundsError(self.balance, amount)
                self.balance -= amount

        account = BankAccount(100)
        account.deposit(50)
        print(account.balance)  # 150

        try:
            account.withdraw(200)
        except InsufficientFundsError as e:
            print(e)  # Cannot withdraw $200: only $150 available
        ```

    The exception carries context (balance and amount) that helps with debugging and user feedback.

---

**Exercise 3.**
Write a `try`/`except` block that catches `InsufficientFundsError` specifically, then a broader `BankError`, demonstrating that exception hierarchy ordering matters in `except` clauses.

??? success "Solution to Exercise 3"

        ```python
        account = BankAccount(50)

        try:
            account.withdraw(100)
        except InsufficientFundsError as e:
            print(f"Specific: {e}")
        except BankError as e:
            print(f"General: {e}")
        ```

    The more specific exception must come first. If `BankError` were listed first, it would catch `InsufficientFundsError` (since it is a subclass), and the specific handler would never execute.
