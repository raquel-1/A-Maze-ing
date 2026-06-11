#!/usr/bin/env python3
"""Module for maze pathfinding using BFS algorithm.

Adheres to PEP 257 and passes strict mypy type checking.
"""

from collections import deque
from typing import Dict, List, Set, Tuple


def find_short_path(
    maze_map: List[List[int]],
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """Find the shortest path through the maze using BFS.

    Args:
        maze_map: 2D grid where each cell is an integer encoding walls.
        entry: (x, y) starting cell coordinates.
        exit_cell: (x, y) destination cell coordinates.

    Returns:
        List of (x, y) tuples from entry to exit (inclusive),
        or an empty list if no path exists.
    """
    if entry == exit_cell:
        return [entry]

    height: int = len(maze_map)
    width: int = len(maze_map[0]) if height > 0 else 0

    # (dx, dy, bit_wall)
    directions: Dict[str, Tuple[int, int, int]] = {
        "N": (0, -1, 1),
        "E": (1, 0, 2),
        "S": (0, 1, 4),
        "W": (-1, 0, 8)
    }

    # BFS utilizing collections.deque for efficient O(1) pops
    waiting_queue: deque[Tuple[int, int]] = deque([entry])
    visited: Set[Tuple[int, int]] = {entry}
    parents: Dict[Tuple[int, int], Tuple[int, int]] = {}

    while waiting_queue:
        actual_x, actual_y = waiting_queue.popleft()

        if (actual_x, actual_y) == exit_cell:
            path: List[Tuple[int, int]] = []
            current: Tuple[int, int] = exit_cell
            while current != entry:
                path.append(current)
                current = parents[current]
            path.append(entry)
            path.reverse()
            return path

        for dx, dy, bit_wall in directions.values():
            # If the bit is set, the wall is closed -> cannot pass
            if maze_map[actual_y][actual_x] & bit_wall:
                continue

            next_x, next_y = actual_x + dx, actual_y + dy

            # Bounds check
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            if (next_x, next_y) not in visited:
                visited.add((next_x, next_y))
                parents[(next_x, next_y)] = (actual_x, actual_y)
                waiting_queue.append((next_x, next_y))

    return []


def convert_path_to_directions(path: List[Tuple[int, int]]) -> str:
    """Convert a list of coordinates into a string of cardinal directions (N, E, S, W).

    Args:
        path: List of (x, y) tuples representing the path.

    Returns:
        A string like "SWSESW..." as required by the output format.
    """
    if len(path) < 2:
        return ""

    string_path: List[str] = []
    
    for i in range(len(path) - 1):
        curr_x, curr_y = path[i]
        next_x, next_y = path[i + 1]
        
        dx: int = next_x - curr_x
        dy: int = next_y - curr_y
        
        if dy == -1:
            string_path.append("N")
        elif dx == 1:
            string_path.append("E")
        elif dy == 1:
            string_path.append("S")
        elif dx == -1:
            string_path.append("W")

    return "".join(string_path)