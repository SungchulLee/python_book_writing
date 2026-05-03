# Enum Practical Patterns

Real-world enum patterns that solve common application needs: state machines, configuration, and domain modeling.

!!! tip "Mental Model"
    Enums shine when you need a closed set of named options with behavior attached. Each pattern on this page replaces scattered `if/elif` logic with methods on the enum itself -- state machines validate transitions, configuration enums carry environment settings, and dispatch enums route to the right handler. The enum becomes the single source of truth for both the values and their semantics.

!!! tip "Pattern Quick Reference"
    | Pattern | When to use | Key technique |
    |---|---|---|
    | State Machine | Workflows with valid transitions | `can_transition_to()` method with transition map |
    | Configuration | Environment-specific settings | `@property` returning config dict |
    | Dispatch / Handler | Route to different logic by type | Method returning handler callable |
    | Roles & Permissions | Access control | `can_perform(action)` with permission sets |
    | Domain Modeling | Rich value objects (cards, menu items) | Tuple values + `@property` accessors |

---

## State Machine Pattern

```python
from enum import Enum
from typing import Optional

class OrderState(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    def can_transition_to(self, next_state) -> bool:
        '''Check if transition is allowed'''
        valid_transitions = {
            OrderState.PENDING: {OrderState.PAID, OrderState.CANCELLED},
            OrderState.PAID: {OrderState.SHIPPED, OrderState.CANCELLED},
            OrderState.SHIPPED: {OrderState.DELIVERED},
            OrderState.DELIVERED: set(),
            OrderState.CANCELLED: set()
        }
        return next_state in valid_transitions.get(self, set())

order_state = OrderState.PENDING
print(order_state.can_transition_to(OrderState.PAID))      # True
print(order_state.can_transition_to(OrderState.SHIPPED))   # False
```

## Configuration with Enums

```python
from enum import Enum
from dataclasses import dataclass

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    
    @property
    def config(self):
        '''Get configuration for environment'''
        configs = {
            Environment.DEVELOPMENT: {
                'debug': True,
                'log_level': 'DEBUG',
                'database_url': 'sqlite:///:memory:'
            },
            Environment.STAGING: {
                'debug': False,
                'log_level': 'INFO',
                'database_url': 'postgresql://staging-db'
            },
            Environment.PRODUCTION: {
                'debug': False,
                'log_level': 'WARNING',
                'database_url': 'postgresql://prod-db'
            }
        }
        return configs[self]

env = Environment.PRODUCTION
config = env.config
print(f"Debug: {config['debug']}, DB: {config['database_url']}")
```

## HTTP Method and Status Codes

```python
from enum import Enum, IntEnum

class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    
    def is_idempotent(self) -> bool:
        '''Check if method is idempotent'''
        idempotent = {HttpMethod.GET, HttpMethod.PUT, HttpMethod.DELETE}
        return self in idempotent

class HttpStatus(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500
    
    @property
    def is_success(self) -> bool:
        '''Check if status indicates success'''
        return 200 <= self.value < 300
    
    @property
    def is_client_error(self) -> bool:
        '''Check if status indicates client error'''
        return 400 <= self.value < 500

method = HttpMethod.PUT
print(f"PUT is idempotent: {method.is_idempotent()}")  # True

status = HttpStatus.CREATED
print(f"201 is success: {status.is_success}")  # True
```

## User Roles and Permissions

```python
from enum import Enum

class UserRole(Enum):
    GUEST = 0
    USER = 1
    MODERATOR = 2
    ADMIN = 3
    
    def can_perform(self, action: str) -> bool:
        '''Check if role can perform action'''
        permissions = {
            'view_content': {UserRole.GUEST, UserRole.USER, UserRole.MODERATOR, UserRole.ADMIN},
            'edit_own': {UserRole.USER, UserRole.MODERATOR, UserRole.ADMIN},
            'edit_others': {UserRole.MODERATOR, UserRole.ADMIN},
            'delete_content': {UserRole.MODERATOR, UserRole.ADMIN},
            'manage_users': {UserRole.ADMIN}
        }
        return self in permissions.get(action, set())

admin = UserRole.ADMIN
user = UserRole.USER

print(f"Admin can manage users: {admin.can_perform('manage_users')}")  # True
print(f"User can manage users: {user.can_perform('manage_users')}")    # False
print(f"User can edit own: {user.can_perform('edit_own')}")            # True
```

## Notification Types and Handling

```python
from enum import Enum
from typing import Callable, Dict

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    
    def get_handler(self) -> Callable:
        '''Get handler function for notification type'''
        handlers = {
            NotificationType.EMAIL: self._send_email,
            NotificationType.SMS: self._send_sms,
            NotificationType.PUSH: self._send_push,
            NotificationType.WEBHOOK: self._send_webhook
        }
        return handlers[self]
    
    @staticmethod
    def _send_email(message: str) -> bool:
        print(f"Sending email: {message}")
        return True
    
    @staticmethod
    def _send_sms(message: str) -> bool:
        print(f"Sending SMS: {message}")
        return True
    
    @staticmethod
    def _send_push(message: str) -> bool:
        print(f"Sending push notification: {message}")
        return True
    
    @staticmethod
    def _send_webhook(message: str) -> bool:
        print(f"Posting webhook: {message}")
        return True

notif_type = NotificationType.EMAIL
handler = notif_type.get_handler()
handler("Hello, World!")
```

## File Type and Handler

```python
from enum import Enum

class FileType(Enum):
    JSON = ".json"
    CSV = ".csv"
    XML = ".xml"
    YAML = ".yaml"
    
    @property
    def parser_module(self) -> str:
        '''Get module name for parsing this file type'''
        modules = {
            FileType.JSON: "json",
            FileType.CSV: "csv",
            FileType.XML: "xml.etree.ElementTree",
            FileType.YAML: "yaml"
        }
        return modules[self]
    
    def validate_content(self, content: str) -> bool:
        '''Basic validation for file type'''
        validators = {
            FileType.JSON: lambda c: c.strip().startswith(('{', '[')),
            FileType.CSV: lambda c: True,  # Minimal validation
            FileType.XML: lambda c: c.strip().startswith('<'),
            FileType.YAML: lambda c: True
        }
        return validators[self](content)

file_type = FileType.JSON
print(f"JSON uses: {file_type.parser_module}")      # json
print(f"Valid JSON: {file_type.validate_content('{}')}")  # True
```

## Color and Formatting

```python
from enum import Enum

class ColorCode(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    
    def format_text(self, text: str) -> str:
        '''Format text with ANSI color code'''
        return f"[{self.value}m{text}[0m"

text = "Important!"
print(ColorCode.RED.format_text(text))      # Displays in red
print(ColorCode.GREEN.format_text("Good"))  # Displays in green
```

## Time Period Enums

```python
from enum import Enum
from datetime import timedelta

class TimePeriod(Enum):
    HOURLY = timedelta(hours=1)
    DAILY = timedelta(days=1)
    WEEKLY = timedelta(days=7)
    MONTHLY = timedelta(days=30)
    YEARLY = timedelta(days=365)
    
    def get_seconds(self) -> int:
        '''Get period duration in seconds'''
        return int(self.value.total_seconds())

period = TimePeriod.WEEKLY
print(f"Weekly period: {period.get_seconds()} seconds")  # 604800
```

---

## Runnable Example: `poker_game_example.py`

```python
"""
OOP Case Study: Poker Card Game with Enumerations

A practical OOP example combining Enum, classes, properties,
magic methods, and composition to build a card game simulator.

Topics covered:
- Enum with @unique for card suits
- Dunder methods: __str__, __repr__, __lt__
- @property for computed attributes
- Composition: Poker has Cards, Player has Cards
- List comprehensions with nested loops
- random.shuffle for shuffling

Based on concepts from Python-100-Days example14 and ch06/enum materials.
"""

import random
from enum import Enum, unique


# =============================================================================
# Example 1: Card Suit Enumeration
# =============================================================================

@unique
class Suit(Enum):
    """Card suits as an enumeration.

    @unique ensures no duplicate values.
    Custom __lt__ enables sorting by suit order.
    """
    SPADE = 0
    HEART = 1
    CLUB = 2
    DIAMOND = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @property
    def symbol(self) -> str:
        symbols = {
            Suit.SPADE: 'S', Suit.HEART: 'H',
            Suit.CLUB: 'C', Suit.DIAMOND: 'D',
        }
        return symbols[self]


# =============================================================================
# Example 2: Card Class
# =============================================================================

class Card:
    """A playing card with suit and face value.

    Face values: 1=Ace, 2-10, 11=Jack, 12=Queen, 13=King
    """

    FACE_NAMES = {
        1: 'A', 11: 'J', 12: 'Q', 13: 'K'
    }

    def __init__(self, suit: Suit, face: int):
        self.suit = suit
        self.face = face

    def __str__(self):
        face_str = self.FACE_NAMES.get(self.face, str(self.face))
        return f'{self.suit.symbol}{face_str}'

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        """Sort by suit first, then by face value."""
        if self.suit != other.suit:
            return self.suit < other.suit
        return self.face < other.face


# =============================================================================
# Example 3: Deck Class (Composition)
# =============================================================================

class Deck:
    """A standard 52-card deck.

    Demonstrates:
    - List comprehension with nested loops
    - @property for state checking
    - Iterator-like dealing interface
    """

    def __init__(self):
        self._index = 0
        self._cards = [
            Card(suit, face)
            for suit in Suit
            for face in range(1, 14)
        ]

    def shuffle(self) -> None:
        """Shuffle the deck and reset the deal position."""
        self._index = 0
        random.shuffle(self._cards)

    def deal(self) -> Card:
        """Deal the next card from the deck.

        Raises:
            IndexError: If no more cards to deal.
        """
        if not self.has_cards:
            raise IndexError("No more cards in deck")
        card = self._cards[self._index]
        self._index += 1
        return card

    @property
    def has_cards(self) -> bool:
        """Check if there are cards remaining to deal."""
        return self._index < len(self._cards)

    @property
    def remaining(self) -> int:
        """Number of cards remaining in deck."""
        return len(self._cards) - self._index

    def __len__(self):
        return len(self._cards)


# =============================================================================
# Example 4: Player Class
# =============================================================================

class Player:
    """A card game player who can receive and organize cards."""

    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] = []

    def receive(self, card: Card) -> None:
        """Add a card to the player's hand."""
        self.hand.append(card)

    def sort_hand(self) -> None:
        """Sort cards in hand by suit and face value."""
        self.hand.sort()

    def show_hand(self) -> str:
        """Display the player's hand."""
        return f"{self.name}: {self.hand}"

    def __repr__(self):
        return f"Player('{self.name}', {len(self.hand)} cards)"


# =============================================================================
# Example 5: Game Simulation
# =============================================================================

def deal_game(num_players: int = 4, cards_each: int = 13) -> None:
    """Simulate dealing cards to players."""
    player_names = ['North', 'East', 'South', 'West']

    deck = Deck()
    deck.shuffle()

    players = [Player(name) for name in player_names[:num_players]]

    print(f"=== Dealing {cards_each} cards to {num_players} players ===")
    print(f"Deck size: {len(deck)} cards")
    print()

    # Deal cards round-robin
    for _ in range(cards_each):
        for player in players:
            if deck.has_cards:
                player.receive(deck.deal())

    # Sort and display each player's hand
    for player in players:
        player.sort_hand()
        print(player.show_hand())

    print(f"\nRemaining in deck: {deck.remaining}")


# =============================================================================
# Example 6: Enum Iteration and Access Patterns
# =============================================================================

def demo_enum_features():
    """Demonstrate Enum features used in this example."""
    print("\n=== Enum Features ===")

    # Iteration
    print("All suits:", [s.name for s in Suit])
    print("All values:", [s.value for s in Suit])

    # Access by name and value
    print(f"By name: Suit['HEART'] = {Suit['HEART']}")
    print(f"By value: Suit(2) = {Suit(2)}")

    # Comparison
    print(f"SPADE < HEART: {Suit.SPADE < Suit.HEART}")

    # Identity
    print(f"Suit.SPADE is Suit(0): {Suit.SPADE is Suit(0)}")


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    deal_game()
    demo_enum_features()
```

## Choosing the Right Enum Type

!!! tip "Enum Decision Guide"

    **Use `Enum` when:**

    - You need a fixed set of named constants with type safety
    - Values represent domain concepts (states, roles, categories)
    - You want to prevent accidental comparisons with raw values

    **Use `Flag` when:**

    - Multiple options can be active simultaneously (permissions, features, config flags)

    **Use `IntEnum` when:**

    - Interacting with numeric APIs, C libraries, or legacy code expecting integers

    **Use `StrEnum` when:**

    - Interacting with string-based systems (JSON, HTTP headers, config files)

    **Avoid enums when:**

    - Values are dynamic or come from external sources at runtime
    - The set of values changes frequently
    - You need hundreds of members (use a dictionary or database instead)

---

## Exercises

**Exercise 1.**
Implement a simple state machine for a `TrafficLight` using an enum. States are `RED`, `YELLOW`, `GREEN`. Add a `next_state` property that cycles through the states in order (GREEN -> YELLOW -> RED -> GREEN). Simulate 6 state transitions.

??? success "Solution to Exercise 1"

        from enum import Enum

        class TrafficLight(Enum):
            GREEN = "green"
            YELLOW = "yellow"
            RED = "red"

            @property
            def next_state(self):
                order = [TrafficLight.GREEN, TrafficLight.YELLOW, TrafficLight.RED]
                idx = order.index(self)
                return order[(idx + 1) % len(order)]

        light = TrafficLight.GREEN
        for _ in range(6):
            print(f"{light.name} -> ", end="")
            light = light.next_state
        print(light.name)

---

**Exercise 2.**
Create a `MenuItem` enum for a restaurant with values as `(price, category)` tuples. Categories are "appetizer", "main", "dessert". Add a class method `by_category(cat)` that returns all items in a given category. Add a class method `cheapest()` that returns the item with the lowest price.

??? success "Solution to Exercise 2"

        from enum import Enum

        class MenuItem(Enum):
            SOUP = (5.99, "appetizer")
            SALAD = (7.99, "appetizer")
            STEAK = (24.99, "main")
            PASTA = (14.99, "main")
            CAKE = (8.99, "dessert")
            ICE_CREAM = (6.99, "dessert")

            @property
            def price(self):
                return self.value[0]

            @property
            def category(self):
                return self.value[1]

            @classmethod
            def by_category(cls, cat):
                return [item for item in cls if item.category == cat]

            @classmethod
            def cheapest(cls):
                return min(cls, key=lambda item: item.price)

        for item in MenuItem.by_category("appetizer"):
            print(f"{item.name}: ${item.price}")

        print(f"Cheapest: {MenuItem.cheapest().name}")

---

**Exercise 3.**
Build a `Command` enum for a CLI application with values as description strings. Members: `HELP`, `VERSION`, `LIST`, `CREATE`, `DELETE`. Add an `execute()` method that prints "Executing: {name} - {description}". Add a class method `from_input(text)` that matches user input (case-insensitive) to a command, returning `None` for unknown commands.

??? success "Solution to Exercise 3"

        from enum import Enum

        class Command(Enum):
            HELP = "Show help information"
            VERSION = "Display version number"
            LIST = "List all items"
            CREATE = "Create a new item"
            DELETE = "Delete an item"

            def execute(self):
                print(f"Executing: {self.name} - {self.value}")

            @classmethod
            def from_input(cls, text):
                try:
                    return cls[text.upper()]
                except KeyError:
                    return None

        cmd = Command.from_input("list")
        if cmd:
            cmd.execute()  # Executing: LIST - List all items

        unknown = Command.from_input("quit")
        print(unknown)  # None

---

**Exercise 4.**
Design a `PaymentState` enum-based state machine with states `CREATED`, `AUTHORIZED`, `CAPTURED`, `REFUNDED`, `FAILED`. Define valid transitions (e.g., `CREATED` can go to `AUTHORIZED` or `FAILED`, but `REFUNDED` is a terminal state). Add a `transition(next_state)` method that raises `ValueError` for invalid transitions. Write a test scenario that processes a payment through its full lifecycle and catches an invalid transition attempt.

??? success "Solution to Exercise 4"

        from enum import Enum

        class PaymentState(Enum):
            CREATED = "created"
            AUTHORIZED = "authorized"
            CAPTURED = "captured"
            REFUNDED = "refunded"
            FAILED = "failed"

            _transitions = {
                "created": {"authorized", "failed"},
                "authorized": {"captured", "failed"},
                "captured": {"refunded"},
                "refunded": set(),
                "failed": set(),
            }

            def transition(self, next_state):
                allowed = self._transitions.value.get(self.value, set())
                if next_state.value not in allowed:
                    raise ValueError(
                        f"Cannot transition from {self.name} to {next_state.name}"
                    )
                return next_state

        # Happy path
        state = PaymentState.CREATED
        state = state.transition(PaymentState.AUTHORIZED)
        state = state.transition(PaymentState.CAPTURED)
        state = state.transition(PaymentState.REFUNDED)
        print(f"Final state: {state.name}")  # REFUNDED

        # Invalid transition
        try:
            state.transition(PaymentState.CAPTURED)
        except ValueError as e:
            print(e)  # Cannot transition from REFUNDED to CAPTURED

---

**Exercise 5.**
Compare two approaches to associating configuration with enum members: (1) a `@property` that returns a dict, and (2) tuple values with `@property` accessors. Implement both for a `Database` enum with members `SQLITE`, `POSTGRES`, `MYSQL`, each having a `driver`, `default_port`, and `supports_json` attribute. Discuss the trade-offs: which is easier to read? Which is easier to extend with new fields?

??? success "Solution to Exercise 5"

        from enum import Enum

        # Approach 1: @property returning dict
        class Database1(Enum):
            SQLITE = "sqlite"
            POSTGRES = "postgres"
            MYSQL = "mysql"

            @property
            def config(self):
                configs = {
                    Database1.SQLITE: {"driver": "sqlite3", "default_port": None, "supports_json": False},
                    Database1.POSTGRES: {"driver": "psycopg2", "default_port": 5432, "supports_json": True},
                    Database1.MYSQL: {"driver": "pymysql", "default_port": 3306, "supports_json": True},
                }
                return configs[self]

        print(Database1.POSTGRES.config["default_port"])  # 5432

        # Approach 2: Tuple values with properties
        class Database2(Enum):
            SQLITE = ("sqlite3", None, False)
            POSTGRES = ("psycopg2", 5432, True)
            MYSQL = ("pymysql", 3306, True)

            def __init__(self, driver, default_port, supports_json):
                self.driver = driver
                self.default_port = default_port
                self.supports_json = supports_json

        print(Database2.POSTGRES.default_port)  # 5432

    **Trade-offs:**

    - **Approach 1** (property dict) is easier to extend with new fields — just add a key to each dict. But access is string-based (`config["driver"]`), which has no IDE autocompletion and risks `KeyError` typos.
    - **Approach 2** (tuple values) gives clean attribute access (`db.driver`) with IDE support, but adding a new field requires updating every member's tuple and the `__init__` signature.
    - For 2–3 fields, approach 2 is cleaner. For many fields or frequently changing schemas, approach 1 or a `dataclass` value is more practical.
