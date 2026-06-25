## Mazegen — Reusable Package

The `mazegen` package contains the maze generation logic as a standalone module
that can be installed and used independently in any Python project.

### Installation

```bash
uv pip install path/mazegen-*.whl
# or
uv pip install path/mazegen-*.tar.gz
```

### Basic Example

```python
from mazegen import MazeGenerator, export_maze_to_file
from mazegen.path_finder import find_short_path

# Create and generate the maze
gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42
)
maze = gen.machete()

# Find the shortest path
path = find_short_path(maze, gen.entry, gen.exit)

# Export to file
export_maze_to_file("maze.txt", gen.entry, gen.exit, maze, path)
```

### MazeGenerator Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `entry` | `tuple[int, int]` | Entry cell as `(x, y)` |
| `exit` | `tuple[int, int]` | Exit cell as `(x, y)` |
| `perfect` | `bool` | `True` = one unique path, `False` = multiple paths |
| `seed` | `int` *(optional)* | Fixed seed for reproducibility. Random if omitted. |

### Accessing the Maze Structure

`gen.machete()` returns a `list[list[int]]` — one integer per cell, encoding
its walls as a bitfield:

| Bit | Value | Wall |
|-----|-------|------|
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

A set bit means the wall is **closed**. For example, `15` (binary `1111`) means
all four walls are closed (isolated cell, used by the `42` pattern).

```python
cell = maze[row][col]
has_north = bool(cell & 1)
has_east  = bool(cell & 2)
has_south = bool(cell & 4)
has_west  = bool(cell & 8)
```

### Regenerating with a New Seed

```python
gen.reset(new_seed=1234)
maze = gen.machete()
```

### Rebuilding the Package from Source

```bash
# In a virtualenv:
pip install build
python -m build
# Output: dist/mazegen-*.whl and dist/mazegen-*.tar.gz
```