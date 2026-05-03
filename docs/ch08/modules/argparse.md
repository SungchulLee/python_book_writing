# Command Line Arguments

The `argparse` module provides a way to parse command-line arguments passed to Python scripts.

!!! tip "Mental Model"
    `argparse` turns your script into a proper command-line tool. You declare what arguments and flags your program accepts, and `argparse` parses `sys.argv`, validates inputs, generates help text, and returns a namespace of clean values. It is the standard-library alternative to manually slicing `sys.argv`.

## Basic Usage

```python
import argparse

parser = argparse.ArgumentParser(description='A simple calculator')
parser.add_argument("num1", type=float, help="First number")
parser.add_argument("num2", type=float, help="Second number")

args = parser.parse_args()
print(f"Sum: {args.num1 + args.num2}")
```

Run:
```bash
python script.py 5 3
# Sum: 8.0
```


## Positional Arguments

Positional arguments are required and parsed in order.

```python
import argparse

def calculate(x, y, op):
    if op == "+": return x + y
    if op == "-": return x - y
    if op == "*": return x * y
    if op == "/": return x / y

parser = argparse.ArgumentParser(description='Calculator')
parser.add_argument("num1", type=float, help="First number")
parser.add_argument("num2", type=float, help="Second number")
parser.add_argument("op", help="Operation: +, -, *, /")

args = parser.parse_args()
result = calculate(args.num1, args.num2, args.op)
print(f"Result: {result}")
```


## Keyword (Optional) Arguments

Use `-` or `--` prefix for optional arguments.

```python
import argparse

parser = argparse.ArgumentParser(description='Calculator')
parser.add_argument("-x", "--num1", type=float, default=0, help="First number")
parser.add_argument("-y", "--num2", type=float, default=0, help="Second number")
parser.add_argument("-o", "--op", default="+", help="Operation")

args = parser.parse_args()
```


## The args Namespace

`parse_args()` returns a `Namespace` object:

```python
args = parser.parse_args()
print(args)  # Namespace(num1=10.0, num2=5.0, op='+')

# Access as attributes
print(args.num1)  # 10.0
print(args.op)    # '+'
```

Use `args.num1`, `args.num2`, and `args.op` to access values safely.

## Exercises

**Exercise 1.** Write a script that uses `argparse` to accept a filename and an optional `--verbose` flag. When `--verbose` is set, print additional information about the file (size, modification time).

??? success "Solution to Exercise 1"

        import argparse
        import os
        import time

        parser = argparse.ArgumentParser(description="Display file info")
        parser.add_argument("filename", help="Path to the file")
        parser.add_argument("--verbose", "-v", action="store_true",
                            help="Show detailed file information")
        args = parser.parse_args()

        if not os.path.exists(args.filename):
            print(f"Error: {args.filename} not found")
        else:
            print(f"File: {args.filename}")
            if args.verbose:
                stat = os.stat(args.filename)
                print(f"  Size: {stat.st_size} bytes")
                print(f"  Modified: {time.ctime(stat.st_mtime)}")

---

**Exercise 2.** Extend the script from Exercise 1 to support subcommands: `info` (display file information) and `count` (count lines, words, and characters in a text file).

??? success "Solution to Exercise 2"

        import argparse
        import os
        import time

        parser = argparse.ArgumentParser(description="File utility")
        subparsers = parser.add_subparsers(dest="command", required=True)

        info_parser = subparsers.add_parser("info", help="Show file info")
        info_parser.add_argument("filename")

        count_parser = subparsers.add_parser("count", help="Count lines/words/chars")
        count_parser.add_argument("filename")

        args = parser.parse_args()

        if args.command == "info":
            stat = os.stat(args.filename)
            print(f"Size: {stat.st_size} bytes")
            print(f"Modified: {time.ctime(stat.st_mtime)}")
        elif args.command == "count":
            with open(args.filename) as f:
                content = f.read()
            lines = content.count("\n")
            words = len(content.split())
            chars = len(content)
            print(f"Lines: {lines}, Words: {words}, Characters: {chars}")

