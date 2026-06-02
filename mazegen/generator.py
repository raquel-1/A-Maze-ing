#!/usr/bin/env python3

import random
from typing import Optional


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: Optional[int] = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        if seed is None:
            self.seed = random.randint(1, 999999)
        else:
            self.seed = seed

        self.my_rand_seed = random.Random(self.seed)

        self.my_map = [[15 for _ in range(width)] for _ in range(height)]

        self.my_visited = [
            [False for _ in range(width)] for _ in range(height)
        ]
        # (dx, dy, bit_wall, bit_oposite)
        self.directions = {
            "N": (0, -1, 1, 4),
            "E": (1, 0, 2, 8),
            "S": (0, 1, 4, 1),
            "W": (-1, 0, 8, 2)
        }

    def machete(self) -> list[list[int]]:
        """Build a maze in the jungle"""

        if self.width >= 9 and self.height >= 7:
            self._42_walls()
        else:
            print(
                "[INFO] Size too small. '42' pattern omitted from rendering."
            )
        self._use_machete(self.entry[0], self.entry[1])
        if not self.perfect:
            self._more_paths()

        return self.my_map

    def _use_machete(self, start_x: int, start_y: int) -> None:
        """stack of explored"""
        pass

    def _42_walls(self) -> None:
        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        four: list[tuple[int, int]] = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
            (2, 3),
            (2, 4)
        ]

        two: list[tuple[int, int]] = [
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        for x, y in four + two:
            x_real_pos = start_x + x
            y_real_pos = start_y + y
            self.my_map[y_real_pos][x_real_pos] = 15
            self.my_visited[y_real_pos][x_real_pos] = True

    def _more_paths(self) -> None:
        pass
