#!/usr/bin/env python3
"""
Sudoku Solver (9x9)
- Input:  0 represents an empty cell.
- Method: Backtracking with MRV (choose cell with fewest candidates).
- Usage:  Put your puzzle in `GRID` or pass a 9-line puzzle via stdin (space/comma separated allowed).

Example row input:
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 6 0 0
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
"""

from typing import List, Optional, Tuple, Set
import sys

Grid = List[List[int]]

def read_grid_from_stdin() -> Optional[Grid]:
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        # accept space/comma separated or contiguous digits
        parts = [p for p in line.replace(",", " ").split() if p]
        if len(parts) == 9:
            try:
                row = [int(x) for x in parts]
            except ValueError:
                return None
            lines.append(row)
        elif len(line) == 9 and all(c.isdigit() for c in line):
            lines.append([int(c) for c in line])
        if len(lines) == 9:
            break
    return lines if len(lines) == 9 else None

def print_grid(grid: Grid) -> None:
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("------+-------+------")
        row = []
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row.append("|")
            row.append(str(grid[r][c]) if grid[r][c] != 0 else ".")
        print(" ".join(row))

def row_vals(grid: Grid, r: int) -> Set[int]:
    return set(grid[r]) - {0}

def col_vals(grid: Grid, c: int) -> Set[int]:
    return {grid[r][c] for r in range(9)} - {0}

def box_vals(grid: Grid, r: int, c: int) -> Set[int]:
    br, bc = (r // 3) * 3, (c // 3) * 3
    return {grid[rr][cc]
            for rr in range(br, br + 3)
            for cc in range(bc, bc + 3)} - {0}

def candidates(grid: Grid, r: int, c: int) -> Set[int]:
    if grid[r][c] != 0:
        return set()
    used = row_vals(grid, r) | col_vals(grid, c) | box_vals(grid, r, c)
    return {d for d in range(1, 10) if d not in used}

def find_mrv_cell(grid: Grid) -> Optional[Tuple[int, int, Set[int]]]:
    """Find the empty cell with the Minimum Remaining Values (fewest candidates)."""
    best = None
    best_cands = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if not cands:
                    return (r, c, set())  # dead end quickly
                if best is None or len(cands) < len(best_cands):
                    best = (r, c)
                    best_cands = cands
                    if len(best_cands) == 1:
                        return (best[0], best[1], best_cands)
    if best is None:
        return None
    return (best[0], best[1], best_cands)

def is_valid_grid(grid: Grid) -> bool:
    # check rows/cols/boxes do not violate constraints
    for r in range(9):
        vals = [v for v in grid[r] if v != 0]
        if len(vals) != len(set(vals)):
            return False
    for c in range(9):
        vals = [grid[r][c] for r in range(9) if grid[r][c] != 0]
        if len(vals) != len(set(vals)):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            vals = []
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    v = grid[r][c]
                    if v != 0:
                        vals.append(v)
            if len(vals) != len(set(vals)):
                return False
    return True

def solve(grid: Grid) -> bool:
    """Mutates grid in place. Returns True if solved."""
    nxt = find_mrv_cell(grid)
    if nxt is None:
        return True  # solved
    r, c, cands = nxt
    if not cands:
        return False
    # simple heuristic: try digits in ascending order
    for d in sorted(cands):
        grid[r][c] = d
        if solve(grid):
            return True
        grid[r][c] = 0
    return False

def copy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]

def main():
    # Example puzzle (0 = blank); comment out if reading from stdin
    GRID: Grid = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,6,0,0],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9],
    ]

    # If user piped a grid in, use that instead
    stdin_grid = read_grid_from_stdin()
    if stdin_grid:
        GRID = stdin_grid

    if not is_valid_grid(GRID):
        print("Invalid puzzle (duplicates in row/col/box).")
        sys.exit(1)

    print("Input:")
    print_grid(GRID)
    work = copy_grid(GRID)
    if solve(work):
        print("\nSolved:")
        print_grid(work)
    else:
        print("\nNo solution exists.")

if __name__ == "__main__":
    main()
