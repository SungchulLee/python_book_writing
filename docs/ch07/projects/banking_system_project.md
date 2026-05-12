# Banking System Project

!!! tip "Mental Model"
    This project models a real banking domain where every account type shares a common interface (`deposit`, `withdraw`, `calculate_interest`) but implements the details differently. The key design insight: inheritance defines the shared contract, and polymorphism lets the bank process any account type without knowing which specific type it is.

## Overview
Build a complete banking system with different account types using inheritance and polymorphism.

## Objectives
- Design a class hierarchy for different account types
- Implement transaction handling
- Apply polymorphism for interest calculation
- Manage customer accounts

## Requirements

### 1. Base Account Class
Create an abstract `BankAccount` class with:

- Attributes: account_number, account_holder, balance, transactions (list)
- Methods:
  - `deposit(amount)` - add money to account
  - `withdraw(amount)` - remove money (check sufficient balance)
  - `get_balance()` - return current balance
  - `get_transaction_history()` - return list of all transactions
  - `apply_fees()` - apply monthly fees (if any)
  - Abstract method: `calculate_interest()` - varies by account type
  - Abstract method: `get_account_type()` - return account type name

### 2. Account Types
Implement these account types:

**SavingsAccount**

- Minimum balance: \$100
- Monthly fee: \$0 (no fee)
- Interest rate: 2% annual (compounded monthly)
- Withdrawal limit: 6 per month
- Penalty: \$5 fee if minimum balance not maintained

!!! note "Compounding Details"
    Monthly compounding means dividing the annual rate by 12 and applying it each
    month to the current balance. Edge cases to handle: what if interest is applied
    mid-month? What if the balance changes during the month? A simple approach is to
    compound based on the balance at the time `apply_interest()` is called.

**CheckingAccount**

- Minimum balance: \$25
- Monthly fee: \$5 (waived if balance > \$500)
- Interest rate: 0.1% annual
- No withdrawal limit
- Overdraft protection: Can go negative up to -\$100 (with \$35 fee)

**BusinessAccount**

- Minimum balance: \$1000
- Monthly fee: \$15
- Interest rate: 1.5% annual
- No withdrawal limit
- Transaction fee: \$0.50 per transaction after 50 transactions/month

**StudentAccount** (inherits from SavingsAccount)

- Minimum balance: \$0
- Monthly fee: \$0
- Interest rate: 1.5% annual
- Withdrawal limit: 10 per month
- Age restriction: Account holder must be student

### 3. Customer Class
Create a `Customer` class with:

- Attributes: customer_id, name, email, accounts (list)
- Methods:
  - `add_account(account)` - open new account
  - `close_account(account_number)` - close account
  - `get_total_balance()` - sum of all account balances
  - `get_all_accounts()` - return list of all accounts
  - `transfer(from_account, to_account, amount)` - move money between accounts

### 4. Bank Class
Create a `Bank` class that:

- Manages all customers and accounts
- Assigns account numbers
- Processes monthly maintenance (fees and interest)
- Generates reports
- Methods:
  - `create_customer(name, email)` - create new customer
  - `find_customer(customer_id)` - find customer by ID
  - `open_account(customer_id, account_type)` - open account for customer
  - `process_monthly_maintenance()` - apply fees and interest to all accounts
  - `get_total_assets()` - sum of all balances
  - `generate_report()` - display bank statistics

!!! warning "Avoid a God Object"
    The `Bank` class risks becoming a "god object" that handles customer management,
    account creation, monthly maintenance, and reporting all in one class. This is the
    most common design mistake in projects like this. Apply the Single Responsibility
    Principle: extract reporting into `BankReporter`, monthly maintenance into
    `MaintenanceProcessor`, and keep `Bank` focused on coordinating these collaborators.
    A good test: if a method doesn't need most of the class's attributes, it probably
    belongs in a separate class.

### 5. Transaction Class
Create a `Transaction` class to track:

- Transaction ID
- Date/time
- Transaction type (deposit, withdrawal, transfer, fee, interest)
- Amount
- Balance after transaction

!!! warning "Data Integrity"
    A production banking system requires atomic transactions: if a transfer debits
    one account but fails to credit the other, the debit must be rolled back.
    Consider implementing a simple rollback mechanism (e.g., wrap the pair of
    operations in a try/except block and undo the debit on failure).

## Sample Usage
```python
# Create bank
bank = Bank("First National Bank")

# Create customer
customer = bank.create_customer("John Doe", "john@email.com")

# Open accounts
savings = bank.open_account(customer.customer_id, "savings")
checking = bank.open_account(customer.customer_id, "checking")

# Perform transactions
savings.deposit(1000)
checking.deposit(500)
checking.withdraw(50)

# Transfer money
customer.transfer(savings, checking, 200)

# Check balances
print(f"Savings: ${savings.get_balance()}")
print(f"Checking: ${checking.get_balance()}")

# Monthly maintenance
bank.process_monthly_maintenance()
```

## Bonus Features
- Add credit card accounts
- Implement loan accounts
- Add transaction categories
- Create account statements
- Add fraud detection
- Implement direct deposit
- Add bill payment system
- Implement simple transaction rollback for failed transfers

## Testing Requirements
Your implementation should:

1. Create multiple customers
2. Open different account types
3. Perform various transactions
4. Test withdrawal limits
5. Test minimum balance violations
6. Test overdraft protection
7. Calculate and apply interest
8. Generate transaction history
9. Test monthly maintenance
10. Generate bank reports

## Files to Create
- `accounts.py` - All account classes
- `customer.py` - Customer class
- `bank.py` - Bank management
- `transaction.py` - Transaction tracking
- `main.py` - Demo program
- `README.md` - This file

Good luck building your bank!

## Exercises

**Exercise 1.**
List all the inheritance and composition relationships in this project. For each, state whether it is "is-a" or "has-a" and justify why that relationship type is appropriate.

??? success "Solution to Exercise 1"

    **Inheritance (is-a):**

    - `SavingsAccount` is-a `BankAccount` — it is a specialized account type with a specific interest rate and withdrawal limit.
    - `CheckingAccount` is-a `BankAccount` — same interface, different rules (overdraft, monthly fee).
    - `BusinessAccount` is-a `BankAccount` — same interface, different fee structure.
    - `StudentAccount` is-a `SavingsAccount` — a more restricted savings account with relaxed minimums.

    **Composition (has-a):**

    - `BankAccount` has-a list of `Transaction` objects — transactions are created by the account and have no meaning outside it.
    - `Customer` has-a list of `BankAccount` objects — a customer owns accounts.
    - `Bank` has-a collection of `Customer` objects — the bank manages customers.

    Inheritance is appropriate here because account types genuinely specialize a common interface (`deposit`, `withdraw`, `calculate_interest`). Composition is appropriate because customers and transactions are independently meaningful entities that are owned or referenced by their containers.

---

**Exercise 2.**
The `Bank.process_monthly_maintenance()` method applies fees and interest to every account. Explain why this method risks making `Bank` a "god object." Sketch a refactored design that extracts this logic into a separate class.

??? success "Solution to Exercise 2"

    `process_monthly_maintenance()` combines two concerns: fee processing and interest calculation. As the system grows (adding statements, compliance checks, notifications), more logic accumulates in `Bank`, violating the Single Responsibility Principle.

    **Refactored design:**

        class MaintenanceProcessor:
            def process(self, accounts):
                for account in accounts:
                    account.apply_fees()
                    interest = account.calculate_interest()
                    if interest > 0:
                        account.deposit(interest)

        class Bank:
            def __init__(self, name):
                self.name = name
                self._customers = {}
                self._maintenance = MaintenanceProcessor()

            def process_monthly_maintenance(self):
                all_accounts = []
                for customer in self._customers.values():
                    all_accounts.extend(customer.get_all_accounts())
                self._maintenance.process(all_accounts)

    Now `Bank` delegates to `MaintenanceProcessor`. Adding a `BankReporter` for `generate_report()` follows the same pattern. Each class has one reason to change.

---

**Exercise 3.**
Implement a simple rollback mechanism for `Customer.transfer()`. If the deposit into the target account fails after the withdrawal from the source account succeeds, the withdrawal must be reversed. Write pseudocode or Python code showing the try/except structure.

??? success "Solution to Exercise 3"

        class Customer:
            def transfer(self, from_account, to_account, amount):
                # Step 1: Withdraw from source
                from_account.withdraw(amount)

                # Step 2: Deposit to target — may fail
                try:
                    to_account.deposit(amount)
                except Exception:
                    # Rollback: reverse the withdrawal
                    from_account.deposit(amount)
                    raise ValueError(
                        f"Transfer failed: could not deposit into "
                        f"{to_account.account_number}. Withdrawal reversed."
                    )

    This ensures that the two accounts stay consistent even when the second operation fails. Production systems use database transactions for atomicity, but this try/except pattern captures the same principle at the application level.

---

**Exercise 4.**
`StudentAccount` inherits from `SavingsAccount`. Explain one scenario where this inheritance could cause a problem (hint: Liskov Substitution Principle). Then propose an alternative design that avoids the issue.

??? success "Solution to Exercise 4"

    **Problem:** `SavingsAccount` enforces a minimum balance of \$100. `StudentAccount` overrides this to \$0. If code expects a `SavingsAccount` and relies on the \$100 minimum (e.g., a function that assumes `withdraw` will reject amounts that leave the balance below \$100), passing a `StudentAccount` may violate that assumption — the student account allows balances that a savings account would reject.

    This is an LSP violation: `StudentAccount` weakens a postcondition (minimum balance guarantee) of its parent class.

    **Alternative design:** Make `StudentAccount` inherit directly from `BankAccount` instead of `SavingsAccount`. Both `SavingsAccount` and `StudentAccount` are siblings with different rules, not parent-child. Shared logic (like withdrawal limit checking) can be extracted into a mixin or utility method rather than forcing an inheritance relationship.
