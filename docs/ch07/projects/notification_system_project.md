# Notification System Project

Real-world applications often need to deliver messages through multiple channels---email, SMS, push notifications, and chat platforms like Slack. When each channel has its own sending and validation logic, abstraction lets you add new channels without modifying the code that dispatches messages. This project exercises the Abstract Base Class patterns introduced earlier in the chapter.

!!! tip "Mental Model"
    This project is the Open/Closed Principle in action: the notification service is open for extension (add a new channel class) but closed for modification (the dispatch logic never changes). The ABC defines the contract (`send`, `validate_recipient`), and each channel implements it independently. Adding Slack support means writing one new class, not touching existing code.

Build a multi-channel notification system using abstraction.

## Requirements

### Abstract NotificationChannel

Define `NotificationChannel` as an abstract base class using Python's `abc` module. It must declare two abstract methods:

- `send(recipient, message)`---Deliver the message to the given recipient via this channel. Raise an exception if delivery fails.
- `validate_recipient(recipient)`---Check that the recipient string is valid for this channel (e.g., email format, phone number format). Return `True` or `False`.

### Implementations

Each concrete class inherits from `NotificationChannel` and implements both abstract methods with channel-specific logic:

- **EmailNotification**---Validate email format, simulate sending via SMTP.
- **SMSNotification**---Validate phone number format, simulate sending via SMS gateway.
- **PushNotification**---Validate device token, simulate push delivery.
- **SlackNotification**---Validate Slack channel or user ID, simulate webhook post.

!!! note "Realistic Validation"
    Basic format checks (e.g., checking for `@` in an email) are a starting point, but production validation goes further. Consider: email---use a regex or a library like `email-validator`; phone numbers---normalize with country codes; device tokens---check length and character set. Robust validation is a key differentiator between a toy project and a realistic one.

### NotificationService

- `register_channel(channel)`---Register a `NotificationChannel` instance for use.
- `send_notification(recipients, message, channels)`---Send the message to all recipients via the specified channels. Handle per-channel failures gracefully by logging the error and continuing with remaining channels.
- Sends via all registered channels if no specific channels are specified.

!!! tip "Adding Depth: Retry and Rate Limiting"
    In production notification systems, transient failures are common (network timeouts, rate limits from providers). Consider adding: (1) a retry mechanism with exponential backoff for failed sends, (2) a per-channel rate limiter to avoid exceeding provider quotas, (3) a message queue so that sends are decoupled from the caller. These additions transform the project from a simple exercise into a realistic system design challenge.

!!! note "Design Pattern: Strategy"
    This architecture follows the **Strategy pattern**: each `NotificationChannel` is an interchangeable strategy for delivering messages. The `NotificationService` depends only on the abstract `NotificationChannel` interface, not on any concrete implementation — this is the **Dependency Inversion Principle** in action. Adding a new channel (e.g., `WhatsAppNotification`) requires only a new class; `NotificationService` needs no changes.

Use Python's `abc` module to define `NotificationChannel` as an abstract base class. Each concrete channel must implement all abstract methods. The `NotificationService` should depend only on the `NotificationChannel` interface, not on any concrete implementation.

### Bonus Features

- Add retry with exponential backoff for failed deliveries
- Implement per-channel rate limiting
- Add a simple in-memory message queue
- Support notification templates with placeholder substitution
- Add delivery status tracking (sent, failed, retrying)
- Log all send attempts with timestamps and outcomes

## Exercises

**Exercise 1.**
Explain how this project applies the Dependency Inversion Principle. What does `NotificationService` depend on? What does it *not* depend on? How does this make it possible to add a new channel without modifying `NotificationService`?

??? success "Solution to Exercise 1"

    `NotificationService` depends on the **abstract interface** `NotificationChannel` — specifically, the `send()` and `validate_recipient()` methods. It does *not* depend on any concrete implementation (`EmailNotification`, `SMSNotification`, etc.).

    This inversion means:

    - `NotificationService` calls `channel.send()` and `channel.validate_recipient()` without knowing which channel it is.
    - Adding `WhatsAppNotification` requires only creating a new class that inherits from `NotificationChannel` and implements both abstract methods.
    - `NotificationService` code is unchanged — it already works with any `NotificationChannel`.

    This is the Dependency Inversion Principle: high-level modules (the service) depend on abstractions (the ABC), not on low-level modules (concrete channels).

---

**Exercise 2.**
Design a retry mechanism with exponential backoff for `NotificationService.send_notification()`. Describe the algorithm, then write pseudocode or Python code that retries a failed `channel.send()` up to 3 times with delays of 1s, 2s, and 4s.

??? success "Solution to Exercise 2"

        import time

        def send_with_retry(channel, recipient, message, max_retries=3):
            for attempt in range(max_retries + 1):
                try:
                    channel.send(recipient, message)
                    return True  # Success
                except Exception as e:
                    if attempt == max_retries:
                        print(f"Failed after {max_retries + 1} attempts: {e}")
                        return False
                    delay = 2 ** attempt  # 1, 2, 4 seconds
                    print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                    time.sleep(delay)

    Exponential backoff prevents overwhelming a failing service: each retry waits longer than the last. The `2 ** attempt` formula doubles the wait each time. Production systems add jitter (random offset) to prevent thundering-herd problems when many clients retry simultaneously.

---

**Exercise 3.**
`NotificationService.send_notification()` must handle per-channel failures gracefully. Write a version that logs errors and continues with remaining channels instead of stopping on the first failure. Return a summary showing which channels succeeded and which failed.

??? success "Solution to Exercise 3"

        class NotificationService:
            def __init__(self):
                self._channels = []

            def register_channel(self, channel):
                self._channels.append(channel)

            def send_notification(self, recipients, message, channels=None):
                targets = channels or self._channels
                results = {"sent": [], "failed": []}

                for channel in targets:
                    for recipient in recipients:
                        if not channel.validate_recipient(recipient):
                            results["failed"].append((type(channel).__name__, recipient, "invalid recipient"))
                            continue
                        try:
                            channel.send(recipient, message)
                            results["sent"].append((type(channel).__name__, recipient))
                        except Exception as e:
                            results["failed"].append((type(channel).__name__, recipient, str(e)))

                return results

    The key design point: a failure in `EmailNotification` should not prevent `SMSNotification` from running. Each channel-recipient pair is handled independently, and the summary lets the caller decide what to do about failures.

---

**Exercise 4.**
Compare two designs for adding notification templates: (a) each `NotificationChannel` subclass has its own `format_message()` method, and (b) a separate `TemplateEngine` class is injected into `NotificationService`. Which design follows the Single Responsibility Principle better? Which is easier to test?

??? success "Solution to Exercise 4"

    **(a) Per-channel `format_message()`:**

    Each channel knows how to format messages for its medium (e.g., HTML for email, plain text for SMS). This works if formatting is tightly coupled to the channel's delivery mechanism.

    **(b) Separate `TemplateEngine`:**

    A `TemplateEngine` class handles all formatting, and `NotificationService` calls `engine.render(template, context)` before passing the result to `channel.send()`. Channels only handle delivery.

    **SRP analysis:** Option (b) is better — it separates *what to say* (template rendering) from *how to deliver it* (channel logic). With option (a), adding a new template format requires modifying every channel subclass.

    **Testing:** Option (b) is easier to test — you can test `TemplateEngine` independently with pure input/output assertions, and test channels with pre-rendered strings. With option (a), testing formatting requires instantiating each channel and mocking its delivery infrastructure.
