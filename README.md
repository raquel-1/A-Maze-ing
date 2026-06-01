
*This project has been created as part of the 42 curriculum by raqroca- and ceboyero*

# A-Maze-ing

## Description

A maze generator written in Python that reads a configuration file, generates a maze with customizable options, and displays it visually in the terminal. The maze can be perfect (single path between entry and exit) and includes a hidden "42" pattern.

## Instructions

### Requirements

- Python 3.10 or later
- [uv](https://github.com/astral-sh/uv) — fast Python package manager

### Installation

```bash
make install
```

Creates a virtual environment and installs all dependencies automatically.

### Run

```bash
make run
```

Runs the program using the default `config.txt` configuration file.

### Debug

```bash
make debug
```

Runs the program using Python's built-in debugger (`pdb`).

### Lint

```bash
make lint
```

Runs `flake8` and `mypy` with the required flags.

### Clean

```bash
make clean
```

Removes temporary files and caches.

### Build the package

```bash
make build
```

Generates `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` inside `dist/`.
```

