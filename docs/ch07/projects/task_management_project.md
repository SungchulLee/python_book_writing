# Final Project: Object-Oriented Task Management System

!!! tip "Mental Model"
    This project ties together all four OOP pillars: classes model the domain (User, Task, Project), encapsulation protects state (task status transitions), inheritance enables specialization (BugTask, FeatureTask), and composition wires the pieces together (a Project *has* Tasks, a User *has* Tasks). Think of it as building a small application where each OOP concept solves a concrete problem.

## Project Overview
Build a complete task management application using object-oriented programming principles. This project will test your understanding of classes, objects, inheritance, encapsulation, and composition.

## Requirements

### 1. User Class
Create a `User` class with the following:

**Attributes:**

- username (string, unique)
- email (string)
- created_at (datetime)
- tasks (list of Task objects)

**Methods:**

- `add_task(task)`: Add a task to user's task list
- `remove_task(task_id)`: Remove task by ID
- `get_tasks()`: Return all tasks
- `get_tasks_by_status(status)`: Filter tasks by status
- `get_tasks_by_priority(priority)`: Filter tasks by priority
- `get_completed_percentage()`: Return percentage of completed tasks
- `__str__()`: Return formatted user info

### 2. Task Class
Create a `Task` class with the following:

**Attributes:**

- task_id (unique integer, auto-generated)
- title (string)
- description (string)
- status (string: 'pending', 'in_progress', 'completed')
- priority (string: 'low', 'medium', 'high')
- created_at (datetime)
- due_date (datetime, optional)
- tags (list of strings)

**Methods:**

- `mark_completed()`: Set status to completed
- `mark_in_progress()`: Set status to in_progress
- `add_tag(tag)`: Add a tag
- `remove_tag(tag)`: Remove a tag
- `is_overdue()`: Check if task is past due date
- `days_until_due()`: Calculate days remaining
- `__str__()`: Return formatted task info
- `__eq__()`: Compare tasks by task_id

**Class Methods:**

- `from_dict(data)`: Create task from dictionary

### 3. Project Class
Create a `Project` class that groups related tasks:

**Attributes:**

- project_id (unique integer)
- name (string)
- description (string)
- tasks (list of Task objects)
- created_at (datetime)
- status (string: 'active', 'completed', 'archived')

**Methods:**

- `add_task(task)`: Add task to project
- `remove_task(task_id)`: Remove task from project
- `get_progress()`: Return percentage of completed tasks
- `get_task_count()`: Return number of tasks
- `get_overdue_tasks()`: Return list of overdue tasks
- `mark_completed()`: Mark project as completed
- `__str__()`: Return project summary

### 4. TaskManager Class
Create a main `TaskManager` class that coordinates everything:

**Attributes:**

- users (dictionary: username -> User object)
- projects (dictionary: project_id -> Project object)

**Methods:**

- `create_user(username, email)`: Create and register new user
- `get_user(username)`: Retrieve user by username
- `create_project(name, description)`: Create new project
- `get_project(project_id)`: Retrieve project by ID
- `assign_task_to_user(task, username)`: Assign task to user
- `assign_task_to_project(task, project_id)`: Add task to project
- `get_all_tasks()`: Return all tasks across all users
- `search_tasks(keyword)`: Search tasks by keyword in title/description
- `get_tasks_by_tag(tag)`: Find all tasks with specific tag
- `generate_report()`: Create summary report

!!! warning "Avoiding a Bloated Manager"
    As features grow, `TaskManager` risks becoming a "god object" that handles user
    management, project management, search, and reporting all in one class. Consider
    extracting cohesive groups of methods into focused classes: a `SearchService` for
    `search_tasks` and `get_tasks_by_tag`, a `ReportGenerator` for `generate_report`,
    etc. `TaskManager` then delegates to these collaborators, keeping each class focused
    on a single responsibility.

### 5. Additional Features (Bonus)
Implement these for extra challenge:

**Priority Queue for Tasks:**

- Sort tasks by priority and due date

**Recurring Tasks:**

- Create `RecurringTask` subclass that inherits from `Task`
- Add frequency attribute (daily, weekly, monthly)
- Implement `create_next_instance()` method

**Task Dependencies:**

- Add `dependencies` attribute to Task
- Implement `can_start()` method (checks if dependencies completed)

**Notifications:**

- Create `Notification` class
- Generate notifications for due tasks
- Send reminders for overdue tasks

**Statistics:**

- Track average completion time
- Most productive days
- Task completion trends

## Implementation Guidelines

### Code Organization
```
task_management/
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── task.py
│   ├── project.py
│   └── task_manager.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── main.py
└── tests.py
```

### Best Practices
1. Use properties with getters and setters for validation
2. Implement proper encapsulation (private attributes where appropriate)
3. Add docstrings to all classes and methods
4. Use class variables for shared constants
5. Implement special methods (`__str__`, `__repr__`, `__eq__`, etc.)
6. Handle exceptions gracefully
7. Follow PEP 8 style guidelines

!!! note "Domain Layer vs Service Layer"
    The classes in this project naturally split into two layers:

    - **Domain models** — `User`, `Task`, `Project`. These represent the core concepts, hold data, and enforce business rules (e.g., "a task cannot be overdue if it has no due date").
    - **Service/application layer** — `TaskManager`. This coordinates domain models, handles search, and generates reports.

    Keeping this separation clean prevents domain logic from leaking into the manager and keeps domain models testable without the full system.

!!! tip "Defining a Persistence Boundary"
    The in-memory implementation is a good starting point, but real task managers
    persist data. Design your classes so that storage logic is isolated behind a clear
    interface (e.g., a `TaskRepository` class with `save`, `load`, `delete` methods).
    This lets you swap between in-memory storage, JSON files, and a database without
    changing your domain classes. This is the **Repository pattern**.

## Sample Usage

```python
# Initialize system
manager = TaskManager()

# Create users
manager.create_user("alice", "alice@example.com")
manager.create_user("bob", "bob@example.com")

# Get user
alice = manager.get_user("alice")

# Create tasks
task1 = Task(
    title="Complete project proposal",
    description="Write the Q4 project proposal",
    priority="high",
    due_date=datetime(2024, 3, 15)
)
task1.add_tag("work")
task1.add_tag("urgent")

task2 = Task(
    title="Review code",
    description="Review pull requests",
    priority="medium"
)

# Assign tasks
manager.assign_task_to_user(task1, "alice")
alice.add_task(task2)

# Create project
project = manager.create_project("Q4 Initiative", "Major Q4 deliverables")
manager.assign_task_to_project(task1, project.project_id)

# Update task status
task1.mark_in_progress()
task2.mark_completed()

# Query tasks
pending = alice.get_tasks_by_status("pending")
high_priority = alice.get_tasks_by_priority("high")
work_tasks = manager.get_tasks_by_tag("work")

# Generate report
report = manager.generate_report()
print(report)
```

## Testing Requirements

Create a `tests.py` file with test cases for:

1. User creation and task management
2. Task status transitions
3. Project progress calculation
4. Task filtering and searching
5. Overdue task detection
6. Task dependencies (if implemented)

## Deliverables

1. Complete source code with all classes
2. Test file demonstrating functionality
3. README documenting:
   - How to run the program
   - Class structure
   - Example usage
   - Any assumptions made

## Evaluation Criteria

- **Functionality (40%)**: All required features work correctly
- **OOP Principles (30%)**: Proper use of classes, inheritance, encapsulation
- **Code Quality (20%)**: Clean, readable, well-documented code
- **Design (10%)**: Good class design and organization

## Tips for Success

1. Start with the basic classes (User, Task) and test them thoroughly
2. Add complexity gradually (Project, TaskManager)
3. Use inheritance wisely (don't force it where composition is better)
4. Think about the relationships between classes
5. Test each feature as you build it
6. Keep methods focused (single responsibility)
7. Use descriptive variable and method names

## Extensions (Optional)

Once you complete the basic requirements, consider adding:

- Persistent storage (save/load from JSON or database)
- Define a `TaskRepository` interface to decouple domain logic from storage
- Web interface using Flask
- Command-line interface (CLI)
- Task comments and collaboration features
- File attachments
- Task templates
- Time tracking
- Calendar integration
- Export to various formats (CSV, PDF)

Good luck! This project will demonstrate your mastery of OOP concepts.

## Exercises

**Exercise 1.**
List all the composition relationships in this project. For each, explain whether it is **composition** (container owns and creates the part) or **aggregation** (container references an independently-existing part). Justify your answers.

??? success "Solution to Exercise 1"

    - **User has-a list of Tasks** — **Aggregation.** Tasks are created independently and assigned to users via `assign_task_to_user()`. A task can exist before being assigned, and deleting a user does not necessarily destroy the task (it may also belong to a project).
    - **Project has-a list of Tasks** — **Aggregation.** Same reasoning — tasks are shared between users and projects.
    - **TaskManager has-a dict of Users** — **Composition.** Users are created by `TaskManager.create_user()` and live inside the manager's registry.
    - **TaskManager has-a dict of Projects** — **Composition.** Projects are created by `TaskManager.create_project()` and owned by the manager.
    - **Task has-a list of tags** — **Composition.** Tags are simple strings created inside the task; they have no independent existence.

    The key difference: tasks are shared across multiple containers (user + project), so they are aggregated. Users and projects are created and owned by the manager, so they are composed.

---

**Exercise 2.**
The `TaskManager` class has methods for user management, project management, task search, and reporting. Explain why this violates the Single Responsibility Principle. Propose a refactored design with at least two extracted classes, and show how `TaskManager` delegates to them.

??? success "Solution to Exercise 2"

    `TaskManager` has four reasons to change: user logic, project logic, search logic, and reporting logic. This makes it a "god object."

    **Refactored design:**

        class SearchService:
            def search_tasks(self, all_tasks, keyword):
                return [t for t in all_tasks if keyword.lower() in t.title.lower()
                        or keyword.lower() in t.description.lower()]

            def get_tasks_by_tag(self, all_tasks, tag):
                return [t for t in all_tasks if tag in t.tags]

        class ReportGenerator:
            def generate(self, users, projects):
                # Build and return a summary report
                ...

        class TaskManager:
            def __init__(self):
                self.users = {}
                self.projects = {}
                self._search = SearchService()
                self._reporter = ReportGenerator()

            def search_tasks(self, keyword):
                return self._search.search_tasks(self.get_all_tasks(), keyword)

            def generate_report(self):
                return self._reporter.generate(self.users, self.projects)

    Now each class has one responsibility. Testing `SearchService` requires no users or projects — just a list of tasks.

---

**Exercise 3.**
Design the `RecurringTask` subclass. It should inherit from `Task` and add a `frequency` attribute (`"daily"`, `"weekly"`, `"monthly"`). Implement a `create_next_instance()` method that returns a new `Task` with the same title, description, and priority, but a new `due_date` shifted by the appropriate interval. Explain why inheritance (not composition) is appropriate here.

??? success "Solution to Exercise 3"

        from datetime import timedelta

        class RecurringTask(Task):
            FREQUENCY_DAYS = {"daily": 1, "weekly": 7, "monthly": 30}

            def __init__(self, title, description, priority, due_date, frequency):
                super().__init__(title, description, priority, due_date)
                if frequency not in self.FREQUENCY_DAYS:
                    raise ValueError(f"Invalid frequency: {frequency}")
                self.frequency = frequency

            def create_next_instance(self):
                delta = timedelta(days=self.FREQUENCY_DAYS[self.frequency])
                next_due = self.due_date + delta
                return RecurringTask(
                    self.title, self.description, self.priority,
                    next_due, self.frequency
                )

    Inheritance is appropriate because a `RecurringTask` **is-a** `Task` — it has all the same attributes and methods (title, status, `mark_completed()`, etc.) plus additional behavior. Any code that works with `Task` also works with `RecurringTask` (LSP holds). Composition would require wrapping a `Task` and re-exposing all its methods, which adds indirection without benefit.

---

**Exercise 4.**
Explain the difference between the **domain layer** (`User`, `Task`, `Project`) and the **service layer** (`TaskManager`) in this project. Give an example of a business rule that belongs in the domain layer and one that belongs in the service layer. What goes wrong if you put domain logic in the service layer?

??? success "Solution to Exercise 4"

    **Domain layer** — classes that represent core concepts and enforce their own invariants:

    - `Task.is_overdue()` — a task knows whether it is past due based on its own `due_date` and `status`.
    - `User.get_completed_percentage()` — a user knows how to compute its own completion rate.

    **Service layer** — classes that coordinate multiple domain objects:

    - `TaskManager.assign_task_to_user()` — involves looking up a user and a task, then connecting them.
    - `TaskManager.generate_report()` — aggregates data across all users and projects.

    **What goes wrong:** if `TaskManager` contains `is_overdue()` logic (e.g., `if task.due_date < now and task.status != "completed"`), the rule is duplicated whenever another class needs to check overdue status. The domain object should own its own rules — the service layer orchestrates, it does not enforce.
