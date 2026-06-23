#!/usr/bin/env python3

from typing import Any, Dict, List, Set, Tuple
import mlx
from mazegen.generator import MazeGenerator
from path_finder import find_short_path


class MazeDisplay:
    def __init__(
            self, width: int, height: int, entry: Tuple[int, int],
            exit: Tuple[int, int], grid: List[List[int]],
            generator: MazeGenerator
    ) -> None:
        """
        Constructor: Set up dimensions, grid, and color palettes.
        """
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.grid: List[List[int]] = grid
        self.generator: MazeGenerator = generator

        self.shortest_path: List[Tuple[int, int]] = find_short_path(
            self.grid, self.entry, self.exit
        )

        self.palettes: List[Dict[str, int]] = [
            {
                "wall":      0x711F47FF,
                "floor":     0x19E6FFFF,
                "entry":     0x6CC00CFF,
                "exit":      0xD2FAFFFF,
                "path":      0xF2C659FF,
                "secret_42": 0x9B81EFFF
            },
            {
                "wall":      0x2B3623FF,
                "floor":     0x8CB21BFF,
                "entry":     0x586AE8FF,
                "exit":      0x5BD4FEFF,
                "path":      0xC5C79BFF,
                "secret_42": 0xEAEEEFFF
            },
            {
                "wall":      0x2F2216FF,
                "floor":     0xE83F6CFF,
                "entry":     0xAD4BB6FF,
                "exit":      0xAD4BB6FF,
                "path":      0xCBC7C2FF,
                "secret_42": 0xFFFFFFFF
            },
            {
                "wall":      0x4BC2FFFF,
                "floor":     0x6B600EFF,
                "entry":     0xA6971AFF,
                "exit":      0xF1F4FFFF,
                "path":      0xAEB3FFFF,
                "secret_42": 0x6870F4FF
            },
            {
                "wall":      0x00F773FF,
                "floor":     0xFF1500FF,
                "entry":     0xFF0084FF,
                "exit":      0x00FE90FF,
                "path":      0x00A1FFFF,
                "secret_42": 0xF7FF00FF
            }
        ]

        self.is_drawing: bool = False

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        self.four: List[Tuple[int, int]] = [
            (start_x + 0, start_y + 0), (start_x + 0, start_y + 1),
            (start_x + 0, start_y + 2), (start_x + 1, start_y + 2),
            (start_x + 2, start_y + 2), (start_x + 2, start_y + 3),
            (start_x + 2, start_y + 4)
        ]

        self.two: List[Tuple[int, int]] = [
            (start_x + 4, start_y + 0), (start_x + 5, start_y + 0),
            (start_x + 6, start_y + 0), (start_x + 6, start_y + 1),
            (start_x + 4, start_y + 2), (start_x + 5, start_y + 2),
            (start_x + 6, start_y + 2), (start_x + 4, start_y + 3),
            (start_x + 4, start_y + 4), (start_x + 5, start_y + 4),
            (start_x + 6, start_y + 4)
        ]
        self.has_42: bool = self.width >= 9 and self.height >= 7
        self.palette_index: int = 0
        self.show_path: bool = False

        # scaling based on grid dimension to fit screen
        if self.width > 70 or self.height > 70:
            self.cell_size = 10
            self.wall_thickness = 2
        elif self.width >= 50 or self.height >= 50:
            max_dim = max(self.width, self.height)
            self.cell_size = max(6, 750 // max_dim)
            self.wall_thickness = max(1, self.cell_size // 4)
        else:
            self.cell_size = 20
            self.wall_thickness = 3

        self.menu_height = 90
        window_w = self.width * self.cell_size
        window_h = self.height * self.cell_size + self.menu_height

        self.mlx: Any = mlx.Mlx()
        self.mlx_ptr: Any = self.mlx.mlx_init()
        self.win: Any = self.mlx.mlx_new_window(
            self.mlx_ptr, window_w, window_h, "A-Maze-ing"
        )

        # retain references securely to prevent flickering states
        self.img: Any = None
        self.secret_set: Set[Tuple[int, int]] = set(self.four + self.two)

        self.draw_maze()
        self.mlx.mlx_expose_hook(self.win, self.draw_maze, None)
        self.mlx.mlx_hook(self.win, 33, 0, self.on_close, None)
        self.mlx.mlx_key_hook(self.win, self.handle_keyboard, None)
        self.mlx.mlx_loop(self.mlx_ptr)

    def draw_maze(self, param: Any = None) -> None:
        """
        Render function: Gets the active palette and draws the maze.
        """
        if self.is_drawing:
            return
        self.is_drawing = True

        current_palette = self.palettes[self.palette_index]

        cell_size = self.cell_size
        wall_thickness = self.wall_thickness

        # build the new buffer completely hidden backstage
        new_img = self.mlx.mlx_new_image(
            self.mlx_ptr, self.width * cell_size, self.height * cell_size
        )
        data: bytearray
        bpp: int
        size_line: int
        data, bpp, size_line, _ = self.mlx.mlx_get_data_addr(new_img)
        bytes_per_pixel = bpp // 8

        def put_pixel(x: int, y: int, color: int) -> None:
            offset = y * size_line + x * bytes_per_pixel
            # blue (B)
            data[offset + 0] = (color >> 24) & 0xFF
            # green (G)
            data[offset + 1] = (color >> 16) & 0xFF
            # red (R)
            data[offset + 2] = (color >> 8) & 0xFF
            # alpha (A)
            data[offset + 3] = color & 0xFF

        # O(1) set storage to guarantee zero-lag loop cycles
        path_set: Set[Tuple[int, int]] = set(self.shortest_path)

        # loop through each row (Y) and each column (X)
        for y_cell in range(self.height):
            for x_cell in range(self.width):

                # CALCULATE REAL PIXEL COORDINATES
                x_pixel_start = x_cell * cell_size
                y_pixel_start = y_cell * cell_size

                cell_value = self.grid[y_cell][x_cell]

                # CHOOSE AND PAINT BACKGROUND COLOR (Floor / Entry / Exit)
                if self.entry == (x_cell, y_cell):
                    floor_color = current_palette["entry"]
                elif self.exit == (x_cell, y_cell):
                    floor_color = current_palette["exit"]
                # show hide path
                elif self.show_path and (x_cell, y_cell) in path_set:
                    floor_color = current_palette["path"]
                elif self.has_42 and (x_cell, y_cell) in self.secret_set:
                    floor_color = current_palette["secret_42"]
                else:
                    floor_color = current_palette["floor"]

                # Hint: To paint a square chunk of floor, you can use loops
                for py in range(y_pixel_start, y_pixel_start + cell_size):
                    for px in range(x_pixel_start, x_pixel_start + cell_size):
                        put_pixel(px, py, floor_color)

                # CHECK WALLS USING BITWISE AND (&)
                wall_color = current_palette["wall"]

                # N (bit 0 -> value 1)
                if cell_value & 1:
                    for t in range(wall_thickness):
                        for px in range(
                            x_pixel_start, x_pixel_start + cell_size
                        ):
                            put_pixel(px, y_pixel_start + t, wall_color)

                # E (bit 1 -> value 2)
                if cell_value & 2:
                    for t in range(wall_thickness):
                        for py in range(
                            y_pixel_start, y_pixel_start + cell_size
                        ):
                            x_pos = (
                                (x_pixel_start + cell_size) - wall_thickness
                                + t
                            )
                            put_pixel(x_pos, py, wall_color)

                # S (bit 2 -> value 4)
                if cell_value & 4:
                    for t in range(wall_thickness):
                        for px in range(
                            x_pixel_start, x_pixel_start + cell_size
                        ):
                            y_pos = (
                                ((y_pixel_start + cell_size) - wall_thickness)
                                + t
                            )
                            put_pixel(px, y_pos, wall_color)

                # W (bit 3 -> value 8)
                if cell_value & 8:
                    for t in range(wall_thickness):
                        for py in range(
                            y_pixel_start, y_pixel_start + cell_size
                        ):
                            put_pixel(x_pixel_start + t, py, wall_color)

        # push image instantly
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, new_img, 0, 0)

        # destruct previous iteration references -> free memory leak
        if self.img is not None:
            self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)
        self.img = new_img

        # draw menu
        text_color = 0xFFFFFF
        base_y = self.height * cell_size + 8
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win, 10, base_y, text_color, "ESC: quit"
        )
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win, 10, base_y + 16, text_color, "1: colors"
        )
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win, 10, base_y + 32, text_color, "P: path"
        )
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win, 10, base_y + 48, text_color, "R: regen"
        )

        self.mlx.mlx_do_sync(self.mlx_ptr)
        self.is_drawing = False

    def handle_keyboard(self, key: int, param: Any) -> int:
        """
        Event Handler: Changes the palette index or toggles path visibility.
        """
        # ESC
        if key == 65307 or key == 27:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
            return 0

        if self.is_drawing:
            return 0

        # 1 change colors
        elif key == 49:
            self.palette_index = (self.palette_index + 1) % len(self.palettes)
            print(f"Palette changed to index: {self.palette_index}")
            self.draw_maze()

        # P o p show/hide path
        elif key == 112:
            self.show_path = not self.show_path
            print(f"Show path state: {self.show_path}")
            self.draw_maze()

        # R o r regenerate maze
        elif key == 114:
            self.generator.reset()
            self.grid = self.generator.machete()
            self.shortest_path = find_short_path(
                self.grid, self.entry, self.exit
            )
            print(f"Maze regenerated with seed: {self.generator.seed}")
            self.draw_maze()

        return 0

    def on_close(self, param: Any) -> None:
        """
        Event Handler: Closes the window when the X button is clicked.
        """
        if self.img is not None:
            self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)
        self.mlx.mlx_loop_exit(self.mlx_ptr)
