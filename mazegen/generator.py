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
        self.my_directions = {
            "N": (0, -1, 1, 4),
            "E": (1, 0, 2, 8),
            "S": (0, 1, 4, 1),
            "W": (-1, 0, 8, 2)
        }

    def machete(self) -> list[list[int]]:
        """Build a maze in the jungle"""

        if self.width >= 9 and self.height >= 7:
            self._42_walls()
            self._use_machete(self.entry[0], self.entry[1])
        else:
            print(
                "[INFO] Size too small. '42' pattern omitted from rendering."
            )
            self._use_prim(self.entry[0], self.entry[1])

        if not self.perfect:
            self._more_paths()

        return self.my_map

    def _use_machete(self, start_x: int, start_y: int) -> None:
        """stack(backpack) of explored"""
        backpack: list[tuple[int, int]] = [(start_x, start_y)]
        self.my_visited[start_y][start_x] = True

        while len(backpack) > 0:
            # my current cell, the last cell
            actual_x, actual_y = backpack[-1]
            # ("N", "E", "S", "W")
            dir_list = list(self.my_directions.keys())
            # roll the dice seed to shuffle
            self.my_rand_seed.shuffle(dir_list)

            can_continue = False
            # test each address in the list
            for name_dir in dir_list:
                # (dx, dy, bit_wall, bit_oposite)
                dx, dy, bit_wall, bit_oposite = self.my_directions[name_dir]
                # calculate the next macheting
                next_x = actual_x + dx
                next_y = actual_y + dy
                # not go off the map
                if 0 <= next_x < self.width and 0 <= next_y < self.height:
                    # not visited
                    if not self.my_visited[next_y][next_x]:
                        # lead the way
                        self.my_map[actual_y][actual_x] = (
                            self.my_map[actual_y][actual_x] - bit_wall
                        )
                        self.my_map[next_y][next_x] = (
                            self.my_map[next_y][next_x] - bit_oposite
                        )
                        # visited territory
                        self.my_visited[next_y][next_x] = True
                        backpack.append((next_x, next_y))
                        can_continue = True
                        # moved, stop looking for more addresses
                        break
            # step back
            if not can_continue:
                backpack.pop()

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
            self.my_visited[y_real_pos][x_real_pos] = True

    def _use_prim(self, start_x: int, start_y: int) -> None:
        """Prim algorithm (bonus)"""
        # first cell visited
        self.my_visited[start_y][start_x] = True
        # save: (actual_x, actual_y, direccion)
        drop_oil: list[tuple[int, int, str]] = []

        # (0,0,"S") (0,0,"N")...
        for n_e_s_w in self.my_directions.keys():
            drop_oil.append((start_x, start_y, n_e_s_w))

        while len(drop_oil) > 0:
            # choose one i
            choose_rand_n = self.my_rand_seed.randint(0, len(drop_oil) - 1)
            # (0,0,"S") <- delete
            actual_x, actual_y, n_e_s_w = drop_oil.pop(choose_rand_n)

            dx, dy, bit_wall, bit_oposite = self.my_directions[n_e_s_w]
            # calculate next limits and visited?
            next_x, next_y = actual_x + dx, actual_y + dy
            if not (0 <= next_x < self.width and 0 <= next_y < self.height):
                continue
            if self.my_visited[next_y][next_x]:
                continue
            # expand
            self.my_map[actual_y][actual_x] -= bit_wall
            self.my_map[next_y][next_x] -= bit_oposite
            self.my_visited[next_y][next_x] = True

            # add next with nesw
            for nueva_dir in self.my_directions.keys():
                drop_oil.append((next_x, next_y, nueva_dir))

    def _more_paths(self) -> None:
        pass
