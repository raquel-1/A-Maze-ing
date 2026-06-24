#!/usr/bin/env python3

from .path_finder import convert_path_to_directions


def export_maze_to_file(
    filename: str,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    maze_map: list[list[int]],
    path: list[tuple[int, int]]
) -> None:
    """
    Generates the output file
    Hexadecimal matrix, empty line, entry, exit, and path directions.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for row in maze_map:
            linea_hex = "".join(format(cell, "X") for cell in row)
            f.write(linea_hex + "\n")

        f.write("\n")

        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_cell[0]},{exit_cell[1]}\n")

        path_directions = convert_path_to_directions(path)
        f.write(path_directions + "\n")
