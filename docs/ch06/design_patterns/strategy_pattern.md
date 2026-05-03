# Strategy Pattern

The Strategy Pattern lets you define a family of algorithms, encapsulate each one, and make them interchangeable at runtime. In Python, first-class functions replace the strategy classes required in traditional OOP implementations.

!!! tip "Mental Model"
    Instead of hard-coding an algorithm inside a class, pass it in as a function. The class becomes a shell that delegates the "how" to whatever function it receives, so you can swap algorithms at runtime without touching the class itself. In Python, first-class functions make this pattern almost invisible -- no strategy interface needed.

**Key Insight**: "Encapsulate what varies" — the algorithm varies, so pass it as a function parameter. The context class remains algorithm-agnostic.

---

## Core Structure

```python
class Context:
    def __init__(self, ..., strategy=None):
        self.strategy = strategy  # A function reference

    def do_something(self):
        if self.strategy:
            result = self.strategy(self)  # Call the strategy function
        return result

def strategy_a(context):
    # Algorithm A
    return result

def strategy_b(context):
    # Algorithm B
    return result

# Usage — swap strategies without touching Context
context = Context(..., strategy=strategy_a)
```

---

## Example: E-Commerce Discount System

### Data Structures

```python
from decimal import Decimal
from typing import Callable, Optional, Sequence
from dataclasses import dataclass
from typing import NamedTuple


class Customer(NamedTuple):
    name: str
    fidelity: int  # loyalty points


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self):
        return self.price * self.quantity


@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None  # ← strategy function

    def total(self) -> Decimal:
        return sum((item.total() for item in self.cart), start=Decimal(0))

    def due(self) -> Decimal:
        discount = self.promotion(self) if self.promotion else Decimal(0)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'
```

The `Order` class accepts any callable as `promotion`. It doesn't know or care which strategy is used — it just calls it.

### Strategy Functions

```python
def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000+ fidelity points."""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    """10% discount on any line item with 20+ units."""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10+ distinct products."""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)


def new_customer_promo(order: Order) -> Decimal:
    """2% welcome discount for customers with fewer than 50 fidelity points."""
    if order.customer.fidelity < 50:
        return order.total() * Decimal('0.02')
    return Decimal(0)
```

### Using Strategies

```python
joe = Customer('John Doe', 0)      # no fidelity points
ann = Customer('Ann Smith', 1100)  # high fidelity

cart = [
    LineItem('banana', 4, Decimal('.5')),
    LineItem('apple', 10, Decimal('1.5')),
    LineItem('watermelon', 5, Decimal(5)),
]

# No discount
Order(joe, cart)
# <Order total: 17.00 due: 17.00>

# fidelity_promo — Joe has 0 points, no discount
Order(joe, cart, promotion=fidelity_promo)
# <Order total: 17.00 due: 17.00>

# fidelity_promo — Ann has 1100 points, 5% discount
Order(ann, cart, promotion=fidelity_promo)
# <Order total: 17.00 due: 16.15>

# bulk_item_promo — 30 bananas qualifies
banana_cart = [LineItem('banana', 30, Decimal('.5')), LineItem('apple', 10, Decimal('1.5'))]
Order(joe, banana_cart, promotion=bulk_item_promo)
# <Order total: 30.00 due: 28.50>
```

---

## Adding New Strategies

No modifications to `Order` needed — just write a new function:

```python
def flash_sale_promo(order: Order) -> Decimal:
    """15% discount on all orders during flash sale period."""
    return order.total() * Decimal('0.15')

# Plug it straight in
Order(joe, cart, promotion=flash_sale_promo)
```

This satisfies the **Open/Closed Principle**: open for extension, closed for modification.

---

## Dynamic Strategy Selection

Because strategies are plain functions, they can be stored in lists and selected programmatically:

```python
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order: Order) -> Decimal:
    """Apply whichever promotion gives the largest discount."""
    return max(promo(order) for promo in promos)

Order(ann, cart, promotion=best_promo)
```

---

## Python vs Traditional OOP

=== "Pythonic (functions)"

    ```python
    def fidelity_promo(order):
        if order.customer.fidelity >= 1000:
            return order.total() * Decimal('0.05')
        return Decimal(0)

    order = Order(customer, cart, promotion=fidelity_promo)
    ```

=== "Traditional OOP (classes)"

    ```python
    class Promotion:
        def discount(self, order): ...

    class FidelityPromo(Promotion):
        def discount(self, order):
            if order.customer.fidelity >= 1000:
                return order.total() * Decimal('0.05')
            return Decimal(0)

    order = Order(customer, cart, strategy=FidelityPromo())
    ```

The function-based approach is shorter, requires no inheritance hierarchy, and is easier to test each strategy in isolation.

---

## When to Use the Strategy Pattern

**Use it when:**

- You have multiple interchangeable algorithms for the same task
- You want to swap algorithms at runtime
- You want to eliminate large `if/elif/else` chains
- New strategies should be addable without modifying existing code

**Common applications:**

| Domain | Strategies |
|--------|-----------|
| E-commerce | Discount calculations, shipping methods |
| Payments | Credit card, PayPal, cryptocurrency |
| Sorting | Bubble sort, quicksort, merge sort |
| Rendering | HTML, PDF, JSON output |
| Compression | ZIP, GZIP, BZIP2 |
| Authentication | Password, OAuth, SAML |
| Caching | LRU, FIFO, LFU eviction |

**Skip it when:**

- You only have one or two algorithms that never change
- The algorithms are trivial one-liners
- Client code genuinely needs algorithm-specific knowledge

---

## Summary

| Concept | Description |
|---------|-------------|
| Context | The class that delegates to a strategy (`Order`) |
| Strategy | A callable that implements one algorithm (`fidelity_promo`) |
| Selection | Pass strategy as a constructor or method argument |
| Extension | Add new strategies as new functions — no class changes |
| Python advantage | First-class functions eliminate the need for strategy classes |

**The one-line version**: pass a function where behaviour varies; keep everything else the same.

---

## Exercises

**Exercise 1.**
Implement a `TextProcessor` class that accepts a `strategy` function in its constructor. The strategy should transform a string. Create three strategies: `uppercase_strategy`, `snake_case_strategy` (replaces spaces with underscores and lowercases), and `title_strategy`. Demonstrate switching strategies at runtime.

??? success "Solution to Exercise 1"

        class TextProcessor:
            def __init__(self, strategy):
                self.strategy = strategy

            def process(self, text):
                return self.strategy(text)

        def uppercase_strategy(text):
            return text.upper()

        def snake_case_strategy(text):
            return text.lower().replace(" ", "_")

        def title_strategy(text):
            return text.title()

        processor = TextProcessor(uppercase_strategy)
        print(processor.process("hello world"))   # HELLO WORLD

        processor.strategy = snake_case_strategy
        print(processor.process("Hello World"))   # hello_world

        processor.strategy = title_strategy
        print(processor.process("hello world"))   # Hello World

---

**Exercise 2.**
Build a `Sorter` class that accepts a `key_strategy` function. Create strategies for sorting a list of `(name, score)` tuples by name alphabetically, by score ascending, and by score descending. Use the same `Sorter` instance and swap strategies between sorts.

??? success "Solution to Exercise 2"

        class Sorter:
            def __init__(self, key_strategy):
                self.key_strategy = key_strategy

            def sort(self, items):
                return sorted(items, key=self.key_strategy)

        students = [("Alice", 88), ("Bob", 95), ("Charlie", 72)]

        by_name = lambda item: item[0]
        by_score_asc = lambda item: item[1]
        by_score_desc = lambda item: -item[1]

        sorter = Sorter(by_name)
        print(sorter.sort(students))

        sorter.key_strategy = by_score_asc
        print(sorter.sort(students))

        sorter.key_strategy = by_score_desc
        print(sorter.sort(students))

---

**Exercise 3.**
Create a shipping cost calculator that uses the strategy pattern. Write a `calculate_shipping(weight, strategy)` function and three strategy functions: `standard_shipping` (flat rate plus per-kg cost), `express_shipping` (rate per kg with a minimum charge), and `free_shipping_over_50` (free if the computed cost exceeds a threshold, else standard rate). Demonstrate each.

??? success "Solution to Exercise 3"

        def standard_shipping(weight):
            return 5.0 + weight * 0.5

        def express_shipping(weight):
            return max(10.0, weight * 2.0)

        def free_shipping_over_50(weight):
            cost = standard_shipping(weight)
            return 0.0 if cost > 50.0 else cost

        def calculate_shipping(weight, strategy):
            return strategy(weight)

        print(f"Standard: ${calculate_shipping(10, standard_shipping):.2f}")
        print(f"Express:  ${calculate_shipping(10, express_shipping):.2f}")
        print(f"Free>50:  ${calculate_shipping(10, free_shipping_over_50):.2f}")
        print(f"Free>50:  ${calculate_shipping(100, free_shipping_over_50):.2f}")
