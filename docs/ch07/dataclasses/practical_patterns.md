# Practical Patterns

Real-world dataclass patterns that solve common problems: configuration objects, API models,
and domain entities. These patterns show dataclasses as engineering tools, not just syntax
sugar — they replace boilerplate while remaining fully compatible with the rest of the Python
ecosystem.

!!! tip "Mental Model"
    A dataclass is a structured bag of data with batteries included -- `__init__`, `__repr__`, `__eq__`, and more are generated for free. The practical patterns on this page show how to combine that foundation with properties, `__post_init__`, and `field()` to build production-ready configuration objects, API models, and domain entities without writing boilerplate.

---

## Configuration Objects

```python
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class DatabaseConfig:
    host: str
    port: int = 5432
    username: str = "admin"
    password: str = field(repr=False)  # Don't show in repr
    options: Dict[str, str] = field(default_factory=dict)
    
    @property
    def connection_string(self) -> str:
        return f"postgres://{self.username}@{self.host}:{self.port}"

config = DatabaseConfig("localhost", password="secret")
print(f"Connecting to {config.connection_string}")
```

## API Request/Response Models

```python
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self):
        return asdict(self)

user = User(1, "Alice", "alice@example.com")
print(user.to_dict())
```

## Domain Model with Validation

```python
from dataclasses import dataclass
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

@dataclass
class Order:
    order_id: str
    customer: str
    amount: float
    status: OrderStatus = OrderStatus.PENDING
    
    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if not self.order_id:
            raise ValueError("Order ID required")
    
    def ship(self):
        if self.status != OrderStatus.PENDING:
            raise ValueError("Can only ship pending orders")
        self.status = OrderStatus.SHIPPED
    
    def deliver(self):
        if self.status != OrderStatus.SHIPPED:
            raise ValueError("Can only deliver shipped orders")
        self.status = OrderStatus.DELIVERED

order = Order("ORD-001", "Alice", 99.99)
order.ship()
order.deliver()
print(f"Order {order.order_id}: {order.status.value}")
```

## Nested Dataclasses

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Address:
    street: str
    city: str
    country: str

@dataclass
class Contact:
    email: str
    phone: str

@dataclass
class Company:
    name: str
    address: Address
    contact: Contact
    employees: int = 0

company = Company(
    name="TechCorp",
    address=Address("123 Main St", "San Francisco", "USA"),
    contact=Contact("info@techcorp.com", "555-1234"),
    employees=50
)

print(f"{company.name} in {company.address.city}")
```

## Builder Pattern with Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class QueryBuilder:
    table: str
    where_conditions: list = field(default_factory=list)
    select_fields: list = field(default_factory=lambda: ["*"])
    limit_value: int = None
    
    def where(self, condition: str):
        self.where_conditions.append(condition)
        return self
    
    def select(self, *fields):
        self.select_fields = list(fields)
        return self
    
    def limit(self, count: int):
        self.limit_value = count
        return self
    
    def build(self) -> str:
        query = f"SELECT {', '.join(self.select_fields)} FROM {self.table}"
        if self.where_conditions:
            query += " WHERE " + " AND ".join(self.where_conditions)
        if self.limit_value:
            query += f" LIMIT {self.limit_value}"
        return query

query = (QueryBuilder("users")
         .select("id", "name", "email")
         .where("age > 18")
         .where("country = 'USA'")
         .limit(10)
         .build())

print(query)
```

## Ecosystem Context: dataclass vs pydantic vs attrs

For simple internal data containers, `@dataclass` from the standard library is
sufficient. When your models sit at a system boundary — parsing JSON from an API,
reading user config files, or feeding data into an ORM — consider these alternatives:

| Concern | dataclass | pydantic | attrs |
|---------|-----------|----------|-------|
| Validation | Manual (`__post_init__`) | Declarative, automatic | Declarative (`@validator`) |
| Type coercion | None | Automatic | Via `converter` |
| Serialization | `asdict()` (shallow) | `.model_dump()` / `.model_dump_json()` | `attrs.asdict()` |
| Dependency | Standard library | External (`pip install pydantic`) | External (`pip install attrs`) |
| Performance | Fast creation | Slower (validation overhead) | Fast (slots by default) |

Use `@dataclass` when validation is simple or unnecessary. Reach for pydantic when
you need schema validation at API boundaries, and attrs when you want rich validators
without pydantic's heavier runtime.

!!! danger "Anti-patterns to avoid"

    - **Business-logic-heavy dataclasses**: A dataclass that grows dozens of methods
      and complex state transitions is no longer a data container — it is a
      domain object pretending to be one. Extract behavior into separate service
      classes and keep the dataclass as a plain data carrier.
    - **God objects**: A single dataclass with 20+ fields that represents an entire
      domain (user + preferences + billing + permissions) should be decomposed into
      smaller, focused dataclasses composed together.

## Data Validation with __post_init__

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class EmailList:
    emails: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Validate and normalize emails
        validated = []
        for email in self.emails:
            if '@' in email:
                validated.append(email.lower())
        self.emails = validated
    
    def add_email(self, email: str):
        if '@' in email:
            self.emails.append(email.lower())

email_list = EmailList(["Alice@Example.com", "Bob@Test.com"])
print(email_list.emails)  # ['alice@example.com', 'bob@test.com']
```

---

## Exercises

**Exercise 1.**
Create a `DatabaseConfig` dataclass with fields `host` (str), `port` (int, default `5432`), `database` (str), `user` (str), and `password` (str). Add a `connection_string` property that returns a formatted connection URL. Add a class method `from_env()` that creates a config from environment variables (simulate with a dictionary). Use `field(repr=False)` on `password`.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass, field

        @dataclass
        class DatabaseConfig:
            host: str
            database: str
            user: str
            password: str = field(repr=False)
            port: int = 5432

            @property
            def connection_string(self):
                return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

            @classmethod
            def from_env(cls, env: dict):
                return cls(
                    host=env.get("DB_HOST", "localhost"),
                    port=int(env.get("DB_PORT", "5432")),
                    database=env.get("DB_NAME", "mydb"),
                    user=env.get("DB_USER", "admin"),
                    password=env.get("DB_PASS", "secret"),
                )

        env = {"DB_HOST": "prod-server", "DB_NAME": "app", "DB_USER": "root", "DB_PASS": "s3cret"}
        config = DatabaseConfig.from_env(env)
        print(config)  # password hidden in repr
        print(config.connection_string)

---

**Exercise 2.**
Design an `APIResponse` dataclass with fields `status_code` (int), `body` (dict), `headers` (dict with `default_factory`), and `timestamp` (auto-set in `__post_init__`). Add a `is_success` property and a `json()` method that returns the body as a JSON string. Create responses for success (200) and error (404) cases.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass, field
        from datetime import datetime
        import json

        @dataclass
        class APIResponse:
            status_code: int
            body: dict
            headers: dict = field(default_factory=dict)
            timestamp: str = field(init=False)

            def __post_init__(self):
                self.timestamp = datetime.now().isoformat()

            @property
            def is_success(self):
                return 200 <= self.status_code < 300

            def json(self):
                return json.dumps(self.body, indent=2)

        ok = APIResponse(200, {"data": [1, 2, 3]})
        err = APIResponse(404, {"error": "Not found"})

        print(ok.is_success)   # True
        print(err.is_success)  # False
        print(ok.json())

---

**Exercise 3.**
Build a `TaskList` dataclass that manages a list of `Task` dataclasses. `Task` has `title`, `done` (bool, default `False`), and `priority` (int, default `0`). `TaskList` has a `tasks` field using `default_factory`. Add methods `add(title, priority)`, `complete(title)`, `pending()` (returns incomplete tasks sorted by priority), and `summary()`. Demonstrate the full workflow.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass, field

        @dataclass
        class Task:
            title: str
            done: bool = False
            priority: int = 0

        @dataclass
        class TaskList:
            tasks: list = field(default_factory=list)

            def add(self, title, priority=0):
                self.tasks.append(Task(title, priority=priority))

            def complete(self, title):
                for task in self.tasks:
                    if task.title == title:
                        task.done = True
                        return
                raise ValueError(f"Task not found: {title}")

            def pending(self):
                return sorted(
                    [t for t in self.tasks if not t.done],
                    key=lambda t: t.priority,
                    reverse=True,
                )

            def summary(self):
                total = len(self.tasks)
                done = sum(1 for t in self.tasks if t.done)
                return f"{done}/{total} tasks completed"

        tl = TaskList()
        tl.add("Write tests", priority=3)
        tl.add("Fix bug", priority=5)
        tl.add("Update docs", priority=1)
        tl.complete("Fix bug")

        print(tl.summary())  # 1/3 tasks completed
        for t in tl.pending():
            print(f"  [{t.priority}] {t.title}")
