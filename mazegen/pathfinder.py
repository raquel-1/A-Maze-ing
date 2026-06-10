#!/usr/bin/env python3

def find_short_path(
    maze_map: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Find the shortest path through the maze
    """
    # (dx, dy, bit_wall)
    directions = {
        "N": (0, -1, 1),
        "E": (1, 0, 2),
        "S": (0, 1, 4),
        "W": (-1, 0, 8)
    }

    # queue BFS: list, starting from the beginning
    waiting_queue = [entry]
    visitados = {entry}

    # notebook for remembering the way (Parents Dictionary)
    # { child_cell: parent_cell }
    parents: dict[tuple[int, int], tuple[int, int]] = {}

    # looping
    # to remove the first one, use: actual_cell = waiting_queue.pop(0)

    # instead pop(0), have a reader that starts at position 0
    idx_lector = 0
    while idx_lector < len(waiting_queue):
        # reed cell without delete(pop)
        actual_x, actual_y = waiting_queue[idx_lector]
        idx_lector += 1
        # ... the rest exactly the same .append() ...
        # delete break and print
        break
    print(f"[DEBUG] Pathfinder waiting: {len(directions)}, "
          f"{len(visitados)}, {len(parents)}, {maze_map[0][0]}, {exit_cell}")
    return []
