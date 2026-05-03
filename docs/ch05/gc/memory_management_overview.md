# Memory Management Overview

Python의 메모리 관리는 두 가지 메커니즘이 함께 동작합니다.

!!! tip "Mental Model"
    Python uses a two-layer cleanup system. Reference counting is the fast, automatic first pass -- the moment nothing points to an object, it is freed instantly. The garbage collector is the slower second pass that catches the edge case reference counting misses: circular references where objects keep each other alive with no outside connections.

## Two Mechanisms

### 1. Reference Counting

대부분의 객체는 참조 카운팅으로 즉시 해제됩니다.

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # Count references
```

### 2. Garbage Collection

순환 참조는 주기적인 가비지 컬렉션으로 처리됩니다.

```python
import gc

# Handle cycles
gc.collect()
```

## How They Work Together

```
Object Created
     │
     ▼
┌─────────────────┐
│ Reference Count │ ──→ refcount == 0 ──→ Freed Immediately
└─────────────────┘
     │
     ▼ (refcount > 0 but unreachable)
┌─────────────────┐
│  Cycle GC       │ ──→ Detects cycles ──→ Freed
└─────────────────┘
```

- **Refcount**: 즉각적인 메모리 해제 (대부분의 경우)
- **GC**: 순환 참조 처리 (주기적 실행)

## Summary

- Reference counting: immediate, deterministic
- Garbage collection: handles cycles
- Both work automatically

---

## Exercises

**Exercise 1.**
Write a script that creates an object, prints its reference count using `sys.getrefcount()`, then adds it to a list and a dictionary. Print the reference count after each step, then remove it from both containers and print the final count. Explain in comments why `getrefcount()` reports one more than expected.

??? success "Solution to Exercise 1"
        ```python
        import sys

        obj = [1, 2, 3]
        # getrefcount adds 1 temporary reference for the argument
        print(f"Initial: {sys.getrefcount(obj)}")  # 2

        lst = [obj]
        print(f"After list: {sys.getrefcount(obj)}")  # 3

        d = {"key": obj}
        print(f"After dict: {sys.getrefcount(obj)}")  # 4

        lst.remove(obj)
        print(f"After removing from list: {sys.getrefcount(obj)}")  # 3

        del d["key"]
        print(f"After removing from dict: {sys.getrefcount(obj)}")  # 2
        ```

---

**Exercise 2.**
Create two `Node` objects that form a circular reference. Use `gc.collect()` to clean them up and print the number of collected objects. Then repeat the experiment with `gc.disable()` before creating the cycle, and show that `del` alone does not free them (verify by checking `gc.garbage` or object counts).

??? success "Solution to Exercise 2"
        ```python
        import gc

        class Node:
            def __init__(self, name):
                self.name = name
                self.ref = None

        # With GC enabled
        gc.enable()
        a = Node("A")
        b = Node("B")
        a.ref = b
        b.ref = a
        del a, b
        collected = gc.collect()
        print(f"GC enabled - collected: {collected}")

        # With GC disabled
        gc.disable()
        c = Node("C")
        d = Node("D")
        c.ref = d
        d.ref = c
        del c, d
        # Without gc.collect(), cycles are not freed
        before = len(gc.get_objects())
        gc.enable()
        collected = gc.collect()
        after = len(gc.get_objects())
        print(f"GC disabled then collected: {collected}")
        ```

---

**Exercise 3.**
Write a function `show_memory_mechanisms()` that demonstrates both memory management mechanisms in sequence: (a) create and delete a simple list, showing immediate deallocation via reference counting (check `weakref.ref` returns `None`), and (b) create a circular reference, delete the variables, and show the objects persist until `gc.collect()` is called.

??? success "Solution to Exercise 3"
        ```python
        import weakref
        import gc

        def show_memory_mechanisms():
            # (a) Reference counting: immediate deallocation
            class Temp:
                pass

            obj = Temp()
            ref = weakref.ref(obj)
            print(f"Before del: ref() is None = {ref() is None}")
            del obj
            print(f"After del:  ref() is None = {ref() is None}")
            print("-> Reference counting freed the object immediately\n")

            # (b) Circular reference: needs GC
            class Node:
                def __init__(self):
                    self.ref = None

            a = Node()
            b = Node()
            a.ref = b
            b.ref = a
            ref_a = weakref.ref(a)

            del a, b
            print(f"After del (cycle): ref_a() is None = {ref_a() is None}")

            collected = gc.collect()
            print(f"After gc.collect(): ref_a() is None = {ref_a() is None}")
            print(f"-> GC collected {collected} objects from the cycle")

        show_memory_mechanisms()
        ```
