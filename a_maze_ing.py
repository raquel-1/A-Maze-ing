#!/usr/bin/env python3

from typing import cast
import config_parser
from mazegen.generator import MazeGenerator
from mazegen.pathfinder import find_short_path
from mazegen.exporter import export_maze_to_file


def main() -> None:
    #  read a .txt file using parse
    config = config_parser.parse_config("config.txt")

    width = cast(int, config["width"])
    height = cast(int, config["height"])
    entry = cast(tuple[int, int], config["entry"])
    exit_cell = cast(tuple[int, int], config["exit"])
    perfect = cast(bool, config["perfect"])
    seed = cast(int | None, config.get("seed"))

    generator = MazeGenerator(
        width=width,
        height=height,
        entry=entry,
        exit=exit_cell,
        perfect=perfect,
        seed=seed,
    )

    map = generator.machete()
    path_coordinates = find_short_path(map, entry, exit_cell)
    road_set = set(path_coordinates)

    print(f"\n--- GENERATED MAZE (Seed: {generator.seed}) ---")
    # ceiling of the maze
    print(" " + "_" * (width * 2 - 1))

    for y, row in enumerate(map):
        line = "|"

        for x, cell in enumerate(row):
            # bit 0=N, bit 1=E, bit 2=S, bit 3=W
            has_e = bool(cell & 2)
            has_s = bool(cell & 4)
            # 42
            if cell == 15:
                line += "██"
            else:
                is_path = (x, y) in road_set

                if has_s:
                    line += "_"
                elif is_path:
                    line += "*"
                else:
                    line += " "

                if has_e:
                    line += "|"
                else:
                    if has_s:
                        line += "_"
                    else:
                        line += " "

        print(line)

    export_maze_to_file(
        filename="output_maze.txt",
        entry=entry,
        exit_cell=exit_cell,
        maze_map=map,
        path=path_coordinates
    )
    print("[INFO] File 'output_maze.txt' exported successfully.")


if __name__ == "__main__":
    main()
