# Backtracking

Backtracking is a recursive algorithm pattern that explores possible solutions, abandoning paths when they become invalid. It's used for constraint satisfaction problems.

!!! tip "Mental Model"
    Backtracking is trial-and-error with an undo button. You make a choice, recurse forward, and if you hit a dead end, you undo the choice and try the next option. The recursion tree prunes itself by abandoning invalid branches early, making it far more efficient than brute-force enumeration.

---

## The Backtracking Pattern

1. Choose a candidate solution path
2. Explore recursively
3. If path leads to solution, return it
4. If path is invalid, backtrack and try another path

## N-Queens Problem

```python
def solve_nqueens(n):
    '''Find all valid placements of n queens on n×n board'''
    results = []
    board = []
    
    def is_safe(row, col):
        '''Check if position is safe from other queens'''
        for i in range(row):
            if board[i] == col:  # Same column
                return False
            if abs(board[i] - col) == abs(i - row):  # Diagonal
                return False
        return True
    
    def backtrack(row):
        '''Recursively place queens'''
        if row == n:
            results.append(board[:])  # Found solution
            return
        
        for col in range(n):
            if is_safe(row, col):
                board.append(col)              # Choose
                backtrack(row + 1)             # Explore
                board.pop()                    # Backtrack
    
    backtrack(0)
    return results

solutions = solve_nqueens(4)
print(f"Found {len(solutions)} solutions for 4 queens")  # 2 solutions
```

## Word Search Problem

```python
def word_search(board, word):
    '''Find word in 2D board by tracing paths'''
    if not board or not word:
        return False
    
    visited = set()
    
    def backtrack(row, col, index):
        # Base case: matched entire word
        if index == len(word):
            return True
        
        # Check bounds and visited
        if (row < 0 or row >= len(board) or
            col < 0 or col >= len(board[0]) or
            (row, col) in visited or
            board[row][col] != word[index]):
            return False
        
        # Choose: mark as visited
        visited.add((row, col))
        
        # Explore: try all 4 directions
        result = (backtrack(row + 1, col, index + 1) or
                 backtrack(row - 1, col, index + 1) or
                 backtrack(row, col + 1, index + 1) or
                 backtrack(row, col - 1, index + 1))
        
        # Backtrack: unmark visited
        visited.remove((row, col))
        
        return result
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if backtrack(i, j, 0):
                return True
    return False

board = [["A","B","C","E"],
         ["S","F","C","S"],
         ["A","D","E","E"]]

print(word_search(board, "ABCB"))   # False
print(word_search(board, "SEE"))    # True
```

## Combination Problem

```python
def generate_combinations(n, k):
    '''Generate all combinations of k numbers from 1 to n'''
    results = []
    
    def backtrack(start, combination):
        # Base case: combination is complete
        if len(combination) == k:
            results.append(combination[:])
            return
        
        # Try adding each number
        for i in range(start, n + 1):
            combination.append(i)      # Choose
            backtrack(i + 1, combination)  # Explore
            combination.pop()           # Backtrack
    
    backtrack(1, [])
    return results

print(generate_combinations(4, 2))
# [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
```

## Performance Notes

- Backtracking explores exponential search space
- Pruning (early rejection) is critical for performance
- Best used for constraint satisfaction problems
- Always check validity before exploring deeper

---

## Runnable Example: `backtracking_knights_tour.py`

```python
"""
Backtracking: The Knight's Tour Problem

Backtracking is a systematic trial-and-error approach:
1. Try a candidate solution
2. If it leads to a dead end, undo (backtrack) and try the next option
3. Continue until a solution is found or all options are exhausted

The Knight's Tour: place a knight on a chessboard and visit every
square exactly once using valid knight moves.

Based on concepts from Python-100-Days example05 and ch05/recursion materials.
"""


# =============================================================================
# Example 1: Knight's Tour with Backtracking
# =============================================================================

# Knight's 8 possible L-shaped moves: (row_delta, col_delta)
KNIGHT_MOVES = [
    (-2, -1), (-1, -2), (1, -2), (2, -1),
    (2, 1),   (1, 2),   (-1, 2), (-2, 1),
]


def print_board(board: list[list[int]]) -> None:
    """Display the board with visit order numbers."""
    size = len(board)
    for row in board:
        for col in row:
            print(str(col).center(4), end='')
        print()
    print()


def knights_tour(size: int = 5, start_row: int = 0, start_col: int = 0,
                 find_all: bool = False) -> int:
    """Find knight's tour solutions using backtracking.

    Args:
        size: Board dimension (size x size).
        start_row: Starting row position.
        start_col: Starting column position.
        find_all: If True, find all solutions. If False, stop at first.

    Returns:
        Number of solutions found.
    """
    board = [[0] * size for _ in range(size)]
    solutions = [0]

    def solve(row: int, col: int, step: int) -> bool:
        """Recursively try to complete the tour.

        Backtracking logic:
        1. Place knight at (row, col) with step number
        2. If all squares visited -> solution found
        3. Try all 8 possible next moves
        4. If no move works -> undo placement (backtrack)
        """
        # Check bounds and whether square is already visited
        if not (0 <= row < size and 0 <= col < size and board[row][col] == 0):
            return False

        board[row][col] = step  # Place knight

        if step == size * size:  # All squares visited
            solutions[0] += 1
            print(f"Solution #{solutions[0]}:")
            print_board(board)
            if not find_all:
                return True  # Stop at first solution
            board[row][col] = 0  # Backtrack to find more
            return False

        # Try all 8 knight moves
        for dr, dc in KNIGHT_MOVES:
            if solve(row + dr, col + dc, step + 1):
                return True  # Solution found downstream

        board[row][col] = 0  # Backtrack: undo this placement
        return False

    solve(start_row, start_col, 1)
    return solutions[0]


# =============================================================================
# Example 2: Warnsdorff's Heuristic (optimization)
# =============================================================================

def count_valid_moves(board: list[list[int]], row: int, col: int) -> int:
    """Count how many valid moves exist from position (row, col)."""
    size = len(board)
    count = 0
    for dr, dc in KNIGHT_MOVES:
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == 0:
            count += 1
    return count


def knights_tour_warnsdorff(size: int = 8, start_row: int = 0,
                             start_col: int = 0) -> bool:
    """Knight's tour using Warnsdorff's rule: always move to the square
    with the fewest onward moves.

    This heuristic dramatically reduces backtracking and typically finds
    a solution in O(n^2) time for standard board sizes.
    """
    board = [[0] * size for _ in range(size)]
    board[start_row][start_col] = 1
    row, col = start_row, start_col

    for step in range(2, size * size + 1):
        # Get all valid next positions
        candidates = []
        for dr, dc in KNIGHT_MOVES:
            nr, nc = row + dr, col + dc
            if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == 0:
                moves_from_next = count_valid_moves(board, nr, nc)
                candidates.append((moves_from_next, nr, nc))

        if not candidates:
            return False  # No valid moves - stuck

        # Choose square with fewest onward moves (Warnsdorff's rule)
        candidates.sort()
        _, row, col = candidates[0]
        board[row][col] = step

    print("Solution (Warnsdorff's heuristic):")
    print_board(board)
    return True


# =============================================================================
# Example 3: N-Queens as Another Backtracking Problem
# =============================================================================

def n_queens(n: int = 8) -> int:
    """Count solutions to the N-Queens problem using backtracking.

    Place n queens on an n x n board so no two queens threaten each other.

    >>> n_queens(4)
    2
    >>> n_queens(8)
    92
    """
    solutions = [0]
    cols = set()        # Columns with queens
    diag1 = set()       # row - col diagonals
    diag2 = set()       # row + col diagonals

    def place_queen(row: int):
        if row == n:
            solutions[0] += 1
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue  # Conflict - skip
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            place_queen(row + 1)
            cols.remove(col)        # Backtrack
            diag1.remove(row - col)
            diag2.remove(row + col)

    place_queen(0)
    return solutions[0]


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    # Knight's tour on a small board (5x5)
    print("=== Knight's Tour (5x5, backtracking) ===")
    count = knights_tour(size=5, start_row=0, start_col=0)
    print(f"Found {count} solution(s)\n")

    # Warnsdorff's heuristic on a larger board (8x8)
    print("=== Knight's Tour (8x8, Warnsdorff's heuristic) ===")
    knights_tour_warnsdorff(size=8)

    # N-Queens
    print("=== N-Queens Solutions ===")
    for n in range(4, 11):
        print(f"  {n}-Queens: {n_queens(n)} solutions")
```

---

## Exercises

**Exercise 1.**
Write a backtracking function `generate_parentheses(n)` that returns all combinations of `n` pairs of well-formed parentheses. For example, `generate_parentheses(3)` should return `["((()))", "(()())", "(())()", "()(())", "()()()"]`.

??? success "Solution to Exercise 1"

        def generate_parentheses(n):
            result = []

            def backtrack(current, open_count, close_count):
                if len(current) == 2 * n:
                    result.append(current)
                    return
                if open_count < n:
                    backtrack(current + "(", open_count + 1, close_count)
                if close_count < open_count:
                    backtrack(current + ")", open_count, close_count + 1)

            backtrack("", 0, 0)
            return result

        print(generate_parentheses(3))
        # ['((()))', '(()())', '(())()', '()(())', '()()()']

---

**Exercise 2.**
Implement a `solve_sudoku(board)` function using backtracking that fills in zeros on a 9x9 board (represented as a list of lists). It should return `True` if the board is solvable (modifying it in place) and `False` otherwise. Test with a simple partially-filled board.

??? success "Solution to Exercise 2"

        def solve_sudoku(board):
            def is_valid(board, row, col, num):
                for i in range(9):
                    if board[row][i] == num or board[i][col] == num:
                        return False
                box_r, box_c = 3 * (row // 3), 3 * (col // 3)
                for i in range(box_r, box_r + 3):
                    for j in range(box_c, box_c + 3):
                        if board[i][j] == num:
                            return False
                return True

            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve_sudoku(board):
                                    return True
                                board[row][col] = 0  # Backtrack
                        return False
            return True

        board = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9],
        ]
        print(solve_sudoku(board))  # True
        print(board[0])  # [5, 3, 4, 6, 7, 8, 9, 1, 2]

---

**Exercise 3.**
Write a backtracking function `find_subsets(nums)` that returns all possible subsets of a list of distinct integers. For example, `find_subsets([1, 2, 3])` should return `[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]` (order may vary).

??? success "Solution to Exercise 3"

        def find_subsets(nums):
            result = []

            def backtrack(start, current):
                result.append(current[:])
                for i in range(start, len(nums)):
                    current.append(nums[i])
                    backtrack(i + 1, current)
                    current.pop()  # Backtrack

            backtrack(0, [])
            return result

        subsets = find_subsets([1, 2, 3])
        print(subsets)
        # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
