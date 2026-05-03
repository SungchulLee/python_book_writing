# User Authentication System Project

Authentication systems handle sensitive data — passwords, session tokens, and account state — that must never be exposed or modified directly by external code. Encapsulation enforces these boundaries at the class level, ensuring that password hashes remain hidden, failed-attempt counters cannot be reset arbitrarily, and sessions expire automatically. This project applies the encapsulation patterns introduced earlier in the chapter.

!!! tip "Mental Model"
    This project is encapsulation under pressure: every piece of sensitive state (password hashes, failed-attempt counters, session tokens) must be private, and every mutation must go through a controlled method. The class boundary becomes a security boundary -- if external code can reach `_password_hash` directly, the entire system is compromised.

Build a secure user authentication system using encapsulation.

## Requirements

### User Class

Private attributes (must not be accessible directly from outside the class):

- `_username` — The user's unique identifier.
- `_password_hash` — Stored hash of the password; never the plaintext.
- `_email` — The user's email address.
- `_failed_attempts` — Counter for consecutive failed login attempts.
- `_is_locked` — Whether the account is currently locked.

Properties:

- `username` — Read-only after creation.
- `email` — Validated format on set (must contain `@` and a domain).
- Password — Expose only a setter that hashes the input (e.g., using `hashlib`). No getter; the plaintext is never stored or retrievable.

Methods:

- `authenticate(password)` — Hash the input and compare to `_password_hash`. Increment `_failed_attempts` on failure and reset to zero on success. Lock the account if failures exceed the threshold (default: 3 consecutive attempts; make this configurable).
- `lock_account()` — Set `_is_locked` to `True`.
- `unlock_account()` — Set `_is_locked` to `False` and reset `_failed_attempts` to zero.

!!! warning "Password Security: Salting and Hashing"
    Hashing alone is vulnerable to rainbow-table attacks. Production systems add a unique random **salt** to each password before hashing, so identical passwords produce different hashes. Python's `hashlib` can do this manually, but `bcrypt` or `argon2-cffi` handle salting automatically and use deliberately slow algorithms to resist brute-force attacks. At minimum, students should generate a random salt per user and store it alongside the hash.

### Session Class

Private attributes:

- `_user` — The authenticated `User` instance.
- `_token` — Generated securely using `secrets.token_hex()` or similar.
- `_expiry` — Set to a configurable duration from creation time (e.g., 30 minutes).
- `_is_active` — Automatically becomes `False` when the current time exceeds `_expiry`.

Methods:

- `is_valid()` — Return `True` only if `_is_active` is `True` and the current time has not exceeded `_expiry`.

!!! note "Session Design Considerations"
    This design covers the basics, but production session management adds: (1) **token revocation** — maintain a set of invalidated tokens so that `logout` takes effect immediately, even if the token has not expired; (2) **refresh tokens** — issue a short-lived access token paired with a long-lived refresh token, so users do not need to re-authenticate frequently but compromised tokens expire quickly; (3) **sliding expiry** — reset the expiry timer on each valid request to keep active sessions alive.

### AuthSystem Class

- `register_user(username, password, email)` — Create a new `User`, validate inputs, and store in an internal user registry. Raise an error if the username already exists.
- `login(username, password)` — Look up the user, call `authenticate()`, and create a `Session` if successful. Raise appropriate errors for locked accounts or invalid credentials.
- `logout(token)` — Invalidate the session associated with the given token.

!!! tip "Persistence and Scaling"
    The in-memory user registry works for learning, but consider how the system would scale. Extracting storage behind a `UserRepository` interface (with `save`, `find_by_username`, `delete` methods) lets you swap between an in-memory dict, a JSON file, or a database without changing `AuthSystem` logic. This is the Repository pattern, and it also makes the class easier to test.

Use Python's name-mangling (`_` prefix) and `@property` decorators to enforce encapsulation. No external code should be able to read password hashes or directly modify account lock status.

## Exercises

**Exercise 1.**
Explain why `_password_hash` must be private with no getter. What would go wrong if external code could read the hash? What would go wrong if external code could *set* the hash directly (bypassing the password setter)?

??? success "Solution to Exercise 1"

    **No getter for the hash:** If external code can read `_password_hash`, it can be logged, serialized to JSON, or leaked into error messages. Even though a hash is not the plaintext password, it enables offline brute-force attacks — an attacker can try millions of password candidates against the known hash without touching the authentication system. Keeping the hash unreadable outside the class limits the attack surface.

    **No direct setter for the hash:** If external code can set `_password_hash = some_value`, it can bypass all validation — no strength checks, no salting, no hashing algorithm enforcement. An attacker (or a careless developer) could set the hash to a known value and authenticate as that user. The password setter must hash the input internally so that the class controls the entire process.

    This is encapsulation applied to security: the `User` class is the **only** code path that touches password hashes.

---

**Exercise 2.**
Implement the `authenticate()` method. It should hash the input password (with the stored salt), compare to `_password_hash`, increment `_failed_attempts` on failure, reset on success, and lock the account after 3 consecutive failures. Write the complete method.

??? success "Solution to Exercise 2"

        import hashlib
        import os

        class User:
            MAX_ATTEMPTS = 3

            def __init__(self, username, password, email):
                self._username = username
                self._email = email
                self._salt = os.urandom(16)
                self._password_hash = self._hash_password(password)
                self._failed_attempts = 0
                self._is_locked = False

            def _hash_password(self, password):
                return hashlib.pbkdf2_hmac(
                    "sha256", password.encode(), self._salt, 100_000
                )

            def authenticate(self, password):
                if self._is_locked:
                    raise PermissionError("Account is locked")

                if self._hash_password(password) == self._password_hash:
                    self._failed_attempts = 0
                    return True
                else:
                    self._failed_attempts += 1
                    if self._failed_attempts >= self.MAX_ATTEMPTS:
                        self._is_locked = True
                    return False

        u = User("alice", "secret123", "alice@example.com")
        print(u.authenticate("wrong"))    # False
        print(u.authenticate("wrong"))    # False
        print(u.authenticate("wrong"))    # False — account now locked
        try:
            u.authenticate("secret123")
        except PermissionError as e:
            print(e)  # Account is locked

---

**Exercise 3.**
Design the `Session` class. It should generate a secure token, track expiry, and expose `is_valid()`. Show how `AuthSystem.login()` creates a session and how `AuthSystem.logout()` invalidates it. Handle the edge case where a user logs in while an existing session is still active.

??? success "Solution to Exercise 3"

        import secrets
        from datetime import datetime, timedelta

        class Session:
            def __init__(self, user, duration_minutes=30):
                self._user = user
                self._token = secrets.token_hex(32)
                self._expiry = datetime.now() + timedelta(minutes=duration_minutes)
                self._is_active = True

            @property
            def token(self):
                return self._token

            def is_valid(self):
                return self._is_active and datetime.now() < self._expiry

            def invalidate(self):
                self._is_active = False

        class AuthSystem:
            def __init__(self):
                self._users = {}
                self._sessions = {}  # token -> Session

            def login(self, username, password):
                user = self._users.get(username)
                if user is None:
                    raise ValueError("User not found")
                if not user.authenticate(password):
                    raise ValueError("Invalid credentials")

                # Invalidate existing session if any
                for token, session in list(self._sessions.items()):
                    if session._user._username == username:
                        session.invalidate()
                        del self._sessions[token]

                session = Session(user)
                self._sessions[session.token] = session
                return session.token

            def logout(self, token):
                session = self._sessions.pop(token, None)
                if session:
                    session.invalidate()

---

**Exercise 4.**
Compare two designs for the user registry in `AuthSystem`: (a) an in-memory dictionary, and (b) a `UserRepository` class with `save()`, `find_by_username()`, and `delete()` methods. Explain how the Repository pattern makes the system easier to test and easier to migrate to a database later.

??? success "Solution to Exercise 4"

    **(a) In-memory dictionary:**

        class AuthSystem:
            def __init__(self):
                self._users = {}  # username -> User

            def register_user(self, username, password, email):
                if username in self._users:
                    raise ValueError("Username taken")
                self._users[username] = User(username, password, email)

    Simple, but `AuthSystem` now contains storage logic mixed with authentication logic. Testing requires the full `AuthSystem`; swapping to a database means rewriting `AuthSystem` internals.

    **(b) Repository pattern:**

        class UserRepository:
            def __init__(self):
                self._store = {}

            def save(self, user):
                self._store[user._username] = user

            def find_by_username(self, username):
                return self._store.get(username)

            def delete(self, username):
                self._store.pop(username, None)

        class AuthSystem:
            def __init__(self, user_repo):
                self._repo = user_repo  # Injected dependency

            def register_user(self, username, password, email):
                if self._repo.find_by_username(username):
                    raise ValueError("Username taken")
                self._repo.save(User(username, password, email))

    **Testing:** inject a `UserRepository` with pre-loaded test users — no need to call `register_user()` in every test. **Migration:** create `DatabaseUserRepository` with the same `save`/`find`/`delete` interface, swap it in without changing `AuthSystem`. This is the power of separating storage from logic.
