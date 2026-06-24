#!/usr/bin/env python3

from typing import cast
import config_parser
from mazegen.generator import MazeGenerator
from mazegen.path_finder import find_short_path
from mazegen.exporter import export_maze_to_file

from display import MazeDisplay


def main() -> None:
    config = config_parser.parse_config("config.txt")

    width = cast(int, config["width"])
    height = cast(int, config["height"])
    entry = cast(tuple[int, int], config["entry"])
    exit_cell = cast(tuple[int, int], config["exit"])
    perfect = cast(bool, config["perfect"])
    seed = cast(int | None, config.get("seed"))
    output_file = cast(str, config["output_file"])

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

    export_maze_to_file(
        filename=output_file,
        entry=entry,
        exit_cell=exit_cell,
        maze_map=map,
        path=path_coordinates
    )
    print(f"[INFO] File '{output_file}' exported successfully.")

    print("[INFO] Opening MiniLibX graphical display...")
    display = MazeDisplay(  # noqa: F841
        width=width,
        height=height,
        entry=entry,
        exit=exit_cell,
        grid=map,
        generator=generator
    )


if __name__ == "__main__":
    main()
