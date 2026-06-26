*This project has been created as part of the 42 curriculum by raqroca-, ceboyero.*

---

<div align="center">

# 🧩 A-Maze-ing

**A Python maze generator and interactive visualizer**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![flake8](https://img.shields.io/badge/style-flake8-05122A?style=for-the-badge)
![mypy](https://img.shields.io/badge/types-mypy-2A6DB5?style=for-the-badge)
![42](https://img.shields.io/badge/42-Madrid-00BABC?style=for-the-badge)

</div>

---

## 📋 Description

**A-Maze-ing** is a maze generator written in Python that reads a configuration file, generates a random maze, and displays it visually using the **MiniLibX (MLX)** graphical library.

Key features:
- Randomly generated mazes with **reproducible seeds**
- Support for **perfect mazes** (one unique path between entry and exit)
- Hidden **"42" pattern** embedded in the maze structure
- **Interactive display** with path highlighting and color themes
- Maze data exported to a structured output file (hexadecimal wall encoding)
- Reusable **`mazegen` package** that can be installed independently via `pip`

---

## ⚙️ Instructions

### Requirements

- Python **3.10** or later
- [`uv`](https://github.com/astral-sh/uv) — fast Python package manager

### Installation

```bash
make install
```

Creates a virtual environment (`.venv`) and installs all dependencies, including `mlx` and the `mazegen` package in editable mode.

### Run

```bash
make run
```

Runs the program using the default `config.txt` configuration file.

```bash
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

Runs the program using Python's built-in debugger (`pdb`).

### Lint

```bash
make lint
```

Runs `flake8` and `mypy` with all required flags.

```bash
make lint-strict
```

Runs `mypy --strict` for enhanced type checking.

### Clean

```bash
make clean
```

Removes temporary files, caches, and the output maze file.

### Validate output

```bash
make validate
```

Runs the provided `output_validator.py` script against the generated `output_maze.txt`.

### Build the reusable package

```bash
make build
```

Generates `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` inside `dist/`.


---

## 🗂️ Configuration File

The program is controlled by a plain-text configuration file named **`config.txt`** located at the root of the repository.

### Format rules

- One `KEY=VALUE` pair per line (case-insensitive keys are also accepted)
- Lines beginning with `#` are treated as **comments** and ignored
- All six mandatory keys must be present

### Mandatory keys

| Key           | Type          | Description                                 | Example              |
|---------------|---------------|---------------------------------------------|----------------------|
| `WIDTH`       | `int > 0`     | Number of columns in the maze               | `WIDTH=20`           |
| `HEIGHT`      | `int > 0`     | Number of rows in the maze                  | `HEIGHT=15`          |
| `ENTRY`       | `int,int`     | Entry cell coordinates `(x,y)`              | `ENTRY=0,0`          |
| `EXIT`        | `int,int`     | Exit cell coordinates `(x,y)`               | `EXIT=19,14`         |
| `OUTPUT_FILE` | `string.txt`  | Name of the output file                     | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | `True`/`False`| Whether the maze has a single solution path | `PERFECT=True`       |

### Optional keys

| Key    | Type  | Description                               | Example    |
|--------|-------|-------------------------------------------|------------|
| `SEED` | `int` | Fixed seed for reproducible maze generation | `SEED=42` |

### Default `config.txt`

```ini
# A-Maze-ing default configuration
# Lines starting with # are comments

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

### Error handling

The parser validates all values before generation begins. Errors caught include:

- Missing mandatory key
- Line without `=` separator
- Non-integer value where an integer is expected
- `PERFECT` not set to `True` or `False`
- Coordinates outside the maze bounds
- `ENTRY` equal to `EXIT`
- `ENTRY` or `EXIT` overlapping a "42" pattern cell
- `OUTPUT_FILE` same as the config filename

---

## 🔁 Maze Generation Algorithm

### Algorithm chosen: Recursive Backtracker (Depth-First Search)

The primary algorithm used is the **recursive backtracker** implemented iteratively using a stack (`backpack`). It starts from the entry cell and carves passages by moving to unvisited neighbors in a random shuffled order, backtracking when no unvisited neighbors remain.

```
Start at entry cell → mark visited → push to stack
While stack not empty:
  Current = top of stack
  Shuffle neighbors randomly
  If any unvisited neighbor exists:
    Remove wall between current and neighbor
    Mark neighbor visited → push to stack
  Else:
    Pop current from stack (backtrack)
```

### Why this algorithm?

The recursive backtracker produces **perfect mazes** (spanning trees) with long, winding corridors, which creates an interesting visual result and a genuinely challenging puzzle. It is also:

- Simple to implement iteratively (no actual recursion risk of stack overflow)
- Fast: `O(width × height)` time and space
- Naturally produces a single connected maze with no isolated regions
- Easily seeded for deterministic output

### 🧩 Bonus — Prim's Algorithm

The Prim's algorithm is implemented in `__use_prim()` and activates automatically for mazes too small to contain the "42" pattern (width < 9 or height < 7). Prim's generates mazes with a more uniform, branchy structure.

**Process:**
Unlike the DFS which follows a specific route, Prim's maintains a "frontier list" of edges and expands the maze by choosing random connections from that list.

* Start at entry cell → mark visited → add all neighbors to `drop_oil` (frontier list).
* While `drop_oil` is not empty:
* Select a random frontier from the list.
* If the destination cell has not been visited:
* Remove the wall between the current cell and the neighbor.
* Mark the neighbor as visited.
* Add the new cell's neighbors to `drop_oil`.


* If already visited, discard the frontier.



**Why this algorithm?**
Prim's generates mazes with a more "bushy" appearance, featuring many short branches instead of the long, winding corridors of the DFS. It is ideal for:

* Small spaces where DFS might generate a path that is too direct.
* Achieving a more homogeneous and dense structure.
* Offering a visually distinct alternative to standard generation.

### Imperfect mazes

When `PERFECT=False`, the `__more_paths_braiding()` method removes dead ends by opening extra walls, while the `__check_3x3_square()` guard prevents any 3×3 open zone from appearing.

### "42" pattern

Before generation, 18 cells forming the digits "4" and "2" are pre-marked as visited (fully walled), so the DFS carves around them. The pattern is centered in the maze grid.

---

## 🖥️ Visual Representation

The maze is rendered in a **MiniLibX graphical window**.

### Controls

| Key     | Action                                  |
|---------|-----------------------------------------|
| `R`     | Re-generate a new maze (new random seed) |
| `P`     | Toggle shortest path visibility         |
| `1`     | Cycle through colour palettes           |
| `ESC`   | Quit the program                        |

### Colour palettes

Four built-in palettes cycle with the `1` key. Each palette defines distinct colours for walls, floor, entry, exit, path, and the "42" pattern cells.

### Cell encoding

Each maze cell stores a 4-bit wall mask (hexadecimal digit):

| Bit | Direction | Value |
|-----|-----------|-------|
| 0   | North     | 1     |
| 1   | East      | 2     |
| 2   | South     | 4     |
| 3   | West      | 8     |

A set bit (1) means the wall is **closed**; 0 means **open**. Cell `0xF` (15) = all walls closed (isolated cell, used for "42" pattern).

---

## 📦 Reusable Module — `mazegen`

The maze generation logic is packaged as a standalone Python module installable via `pip`.

### Installation

```bash
uv pip install path/dist/mazegen-1.0.0-py3-none-any.whl
# or
uv pip install path/dist/mazegen-1.0.0.tar.gz
```

### Module Reference

#### `MazeGenerator`

```python
from mazegen.generator import MazeGenerator

gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42          # optional; random if omitted
)

maze_map: list[list[int]] = gen.machete()
# maze_map[y][x] → integer 0–15 encoding the walls of cell (x,y)
```

#### `find_short_path`

```python
from mazegen.path_finder import find_short_path, convert_path_to_directions

path = find_short_path(maze_map, entry=(0, 0), exit_cell=(19, 14))
# path → list of (x, y) tuples

directions = convert_path_to_directions(path)
# directions → "SSEENWW..." string
```

#### `export_maze_to_file`

```python
from mazegen.exporter import export_maze_to_file

export_maze_to_file(
    filename="output.txt",
    entry=(0, 0),
    exit_cell=(19, 14),
    maze_map=maze_map,
    path=path
)
```

#### `gen.reset(new_seed=None)`

Resets the generator with a new (or random) seed so `machete()` can be called again.

#### `get_42_cells(width, height)`

```python
from mazegen.generator import get_42_cells

cells = get_42_cells(20, 15)
# → list of (x, y) occupied by the "42" pattern, empty list if maze is too small
```

### Output file format

```
<HEIGHT lines of WIDTH hex chars>     ← maze wall matrix
                                       ← empty line
x_entry,y_entry                        ← entry coordinates
x_exit,y_exit                          ← exit coordinates
NSEW...                                ← shortest path as cardinal directions
```

---

## 👥 Team & Project Management

### Team members

| Login     | Main responsibilities                                                    |
|-----------|-------------------------------------------------------------------------|
| `raqroca` | Maze generation algorithms (DFS / Prim), "42" pattern, config parser, error handling |
| `ceboyero` | MiniLibX display, colour palettes, keyboard interactions, path visualisation, package build |

### Planning

**1** — Research maze algorithms, design data structures, implement DFS backtracker and basic file export.

**2** — Integrate MLX display, implement BFS path finder, add colour palettes and keyboard controls.

**3** — Add Prim's algorithm, imperfect maze braiding, 3×3 open-area guard, config validation, and `mazegen` packaging.

**4** — Testing, linting (`flake8` + `mypy`), README, and evaluation preparation.

The initial plan was to finish display in week 1, but integrating MLX took longer than expected. We adapted by working in parallel on the generator and display layers.

### What went well

- The DFS algorithm was straightforward to implement and produced great-looking mazes immediately.
- The hexadecimal wall-encoding scheme made both export and display logic clean and efficient.
- Splitting generation into a reusable package from the start kept the codebase organised.

### What could be improved

- The MLX pixel-by-pixel rendering is slow for very large mazes (> 100×100); a tile-based approach would be faster.
- The 3×3 open-area check (`__check_3x3_square`) could be optimised.
- More automated tests for edge cases in the config parser would have saved debugging time.

### Tools used

- **uv** — dependency and virtual environment management
- **flake8** — PEP 8 linting
- **mypy** — static type checking
- **hatchling / build** — Python package build system
- **Claude (AI)** — used to clarify documentation structure and review error-message wording; all algorithmic logic was written and understood by the team members

---

## 📚 Resources

| Resource | Used for |
|----------|----------|
| [Maze generation algorithm recap — Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) | Understanding DFS, Prim's, and other algorithms; choosing the right approach |
| [Python `random` module docs](https://docs.python.org/3/library/random.html) | Seeded randomness for reproducible mazes |
| [BFS — Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) | Efficient shortest-path finder |
| [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/) | Docstring style for all functions and classes |
| [mypy documentation](https://mypy.readthedocs.io/) | Type hints and static checking |
| [hatchling / PyPA packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) | Building the `mazegen` pip-installable package |
| [Coolors — colour palette generator](https://coolors.co/palettes/popular/6%20colors) | Designing the four display colour palettes |
| **Claude (Anthropic AI)** | Reviewed README structure to ensure it matched the subject requirements; helped word clear error messages in `config_parser.py`. No algorithm or display logic was generated by AI — all code was written and is fully understood by the team. |


