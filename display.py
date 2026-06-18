#!/usr/bin/env python3

import mlx
from typing import List, Dict, Any


class MazeDisplay:
    def __init__(self, width: int, height: int, grid: List[List[str]]) -> None:
        """
        Constructor: Set up dimensions, grid, and color palettes.
        """
        self.width: int = width
        self.height: int = height
        self.grid: List[List[str]] = grid

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

        # 2. Track which palette is currently active (starts at 0)
        self.palette_index: int = 0

        # 3. Track if the shortest path should be visible or hidden
        self.show_path: bool = False

        # 4. Initialize MiniLibX and create the window
        # self.init_ptr = mlx.init()
        # self.win_ptr = mlx.new_window(...)

    def draw_maze(self) -> None:
        """
        Render function: Gets the active palette and draws the maze.
        """
        # Get the dictionary of the current color palette
        current_palette = self.palettes[self.palette_index]

        # Now, when you need a color, you grab it from the dictionary!
        # Example:
        # wall_color = current_palette["wall"]
        # floor_color = current_palette["floor"]
        # secret_color = current_palette["secret_42"]

        # TODO: Loop through 'self.grid' and paint using these dynamic colors
        pass

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
