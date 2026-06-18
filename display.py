#!/usr/bin/env python3

import mlx
from typing import List, Dict, Any


class MazeDisplay:
    def __init__(
            self, width: int, height: int, entry: tuple[int, int],
            exit: tuple[int, int], grid: List[List[int]]
    ) -> None:
        """
        Constructor: Set up dimensions, grid, and color palettes.
        """
        self.width: int = width
        self.height: int = height
        self.entry = entry
        self.exit = exit
        self.grid: List[List[int]] = grid

        # 1. Define your list of available palettes (Lists of dictionaries)
        self.palettes: List[Dict[str, int]] = [
            # Index 0: Classic Palette
            # white black green red cian darkgrey
            {
                "wall": 0xFFFFFF,
                "floor": 0x000000,
                "entry": 0x00FF00,
                "exit": 0xFF0000,
                "path": 0x00FFFF,
                "secret_42": 0x444444
            },

            # Index 1: Cyberpunk (Neon Palette)
            # BrightMagenta Verydarkpurple neongreen electricblue darkpurple
            {
                "wall": 0xFF00FF,
                "floor": 0x110022,
                "entry": 0x00FF00,
                "exit": 0xFFFF00,
                "path": 0x00FFFF,
                "secret_42": 0x330033
            }
        ]

        self.four: list[tuple[int, int]] = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
            (2, 3),
            (2, 4)
        ]

        self.two: list[tuple[int, int]] = [
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        # 2. Track which palette is currently active (starts at 0)
        self.palette_index: int = 0

        # 3. Track if the shortest path should be visible or hidden
        self.show_path: bool = False

        # 4. Initialize MiniLibX and create the window
        self.init_ptr = mlx.init()
        self.win_ptr = mlx.new_window(...)

    def draw_maze(self) -> None:
        """
        Render function: Gets the active palette and draws the maze.
        """
        current_palette = self.palettes[self.palette_index]

        # Dimensions for each cell
        cell_size = 40
        wall_thickness = 4

        # Loop through each row (Y) and each column (X)
        for y_cell in range(self.height):
            for x_cell in range(self.width):

                # 1. CALCULATE REAL PIXEL COORDINATES
                x_pixel_start = x_cell * cell_size
                y_pixel_start = y_cell * cell_size

                # 2. Coger el valor
                cell_value = self.grid[y_cell][x_cell]

                # 3. CHOOSE AND PAINT BACKGROUND COLOR (Floor / Entry / Exit)
                # check (x_cell,y_cell) = the entrance or exit to select color
                if (self.entry == (x_cell, y_cell)):
                    floor_color = current_palette["entry"]
                elif self.exit == (x_cell, y_cell):
                    floor_color = current_palette["exit"]
                elif (x_cell, y_cell) in self.four + self.two:
                    floor_color = current_palette["secret_42"]
                else:
                    floor_color = current_palette["floor"]
                # Hint: To paint a square chunk of floor, you can use loops
                for py in range(y_pixel_start, y_pixel_start + cell_size):
                    for px in range(x_pixel_start, x_pixel_start + cell_size):
                        mlx.pixel_put(
                            self.init_ptr, self.win_ptr, px, py, floor_color
                        )

                # 4. CHECK WALLS USING BITWISE AND (&)
                wall_color = current_palette["wall"]

                # North Wall (Bit 0 -> Value 1)
                if cell_value & 1:
                    for t in range(wall_thickness):
                        for px in range(
                            x_pixel_start, x_pixel_start + cell_size
                        ):
                            mlx.pixel_put(
                                self.init_ptr, self.win_ptr, px,
                                y_pixel_start + t, wall_color
                            )

                # East Wall (Bit 1 -> Value 2)
                if cell_value & 2:
                    # Dibujamos la línea vertical en el lado derecho
                    for t in range(wall_thickness):
                        for py in range(
                            y_pixel_start, y_pixel_start + cell_size
                        ):
                            x_pos = (
                                (x_pixel_start + cell_size) - wall_thickness
                                + t
                            )
                            mlx.pixel_put(
                                self.init_ptr, self.win_ptr, x_pos,
                                py, wall_color
                            )

                # South Wall (Bit 2 -> Value 4)
                if cell_value & 4:
                    for t in range(wall_thickness):
                        for px in range(
                            x_pixel_start, x_pixel_start + cell_size
                        ):
                            y_pos = (
                                ((y_pixel_start + cell_size) - wall_thickness)
                                + t
                            )
                            mlx.pixel_put(
                                self.init_ptr, self.win_ptr, px, y_pos,
                                wall_color
                            )

                # West Wall (Bit 3 -> Value 8)
                if cell_value & 8:
                    for t in range(wall_thickness):
                        for py in range(
                            y_pixel_start, y_pixel_start + cell_size
                        ):
                            mlx.pixel_put(
                                self.init_ptr, self.win_ptr, x_pixel_start
                                + t, py, wall_color
                            )

    def handle_keyboard(self, key: int, param: Any) -> int:
        """
        Event Handler: Changes the palette index when key '3' is pressed.
        """
        if key == 65307 or key == 27:  # ESC
            exit(0)

        # Key '3' (usually code 51 in Linux/X11) to change the color palette
        elif key == 51:
            # Cycle to the next palette index smoothly using modulo (%)
            self.palette_index = (self.palette_index + 1) % len(self.palettes)
            print(f"Palette changed to index: {self.palette_index}")

            # CRITICAL: Redraw the maze so changes take effect instantly
            self.draw_maze()

        return 0
