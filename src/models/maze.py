from .cell import Cell
from src.utils.cleanup import clear_img
import random


class Maze:

    def __init__(
        self,
        maze_input: list[str],
        maze_sz: tuple[int, int],
        mlx_data: tuple,
        colors: tuple[tuple[tuple]],
        maze_pos: tuple,
        path: tuple
    ) -> None:

        self.input: list[str] = maze_input
        self.width, self.height = maze_sz
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.toggle_path: bool = False
        self.generated: bool = False
        self.path_displayed: bool = False
        self.coor: tuple = path[1]
        self.path: list[list] = self.parse_path(path[0])
        self.path_coor: list[tuple] = [
            (y, x)
            for y in range(len(self.path))
            for x in range(len(self.path[0]))
            if self.path[y][x]
        ]
        self.maze_pos: tuple = maze_pos
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )
        self.buf, self.bpp, self.sz_line, *oth = (
            self.mlx.mlx_get_data_addr(self.img)
        )
        self.color_palette: tuple = colors
        self.current_colors: tuple = colors[0]
        self.bg_color: int = 1
        self.animating: bool = False
        self.anim_row: int = 0
        self.anim_col: int = 0
        self.frame_delay: int = 1
        self.frame_count: int = 0

    def redraw(self) -> None:

        if not self.generated:
            return None

        clear_img(self.buf)
        self.cells = []

        for row in range(len(self.input)):

            self.cells.append([])

            for col in range(len(self.input[0])):

                self.bg_color = 1

                if self.toggle_path and self.path[row][col]:
                    self.bg_color = 2

                self.cells[row].append(Cell(
                    self.input[row][col],
                    (col, row),
                    self.width // len(self.input[0]),
                    (self.buf, self.sz_line, self.bpp),
                    (
                        self.current_colors[0],
                        self.current_colors[self.bg_color]
                    )
                ))

                self.cells[row][col].draw()

    def start_animation(self) -> None:

        if not self.toggle_path or self.path_displayed:
            clear_img(self.buf)
            self.toggle_path = False
            self.path_displayed = False

        self.generated = True
        self.cells: list[list] = [
            [None for _ in range(len(self.input[0]))]
            for _ in range(len(self.input))
        ]
        self.anim_row = 0
        self.anim_col = 0
        self.animating = True

    def animate_step(self) -> None:

        if not self.animating:
            return None

        self.frame_count += 1
        if self.frame_count < self.frame_delay:
            return None
        self.frame_count = 0

        if self.anim_row >= len(self.input):
            self.animating = False
            return None

        if self.toggle_path:
            if self.cur_path_pos >= len(self.path_coor):
                return None

            self.anim_row, self.anim_col = self.path_coor[
                self.cur_path_pos
            ]

        self.cells[self.anim_row][self.anim_col] = Cell(
            self.input[self.anim_row][self.anim_col],
            (self.anim_col, self.anim_row),
            self.width // len(self.input[0]),
            (self.buf, self.sz_line, self.bpp),
            (
                self.current_colors[0],
                self.current_colors[self.bg_color]
            )
        )

        self.cells[self.anim_row][self.anim_col].draw()

        if not self.toggle_path:
            self.anim_col += 1
            if self.anim_col >= len(self.input[0]):
                self.anim_col = 0
                self.anim_row += 1

        else:
            self.cur_path_pos += 1

    def toggle_path_on_off(self) -> None:

        if not self.generated:
            return None

        self.toggle_path = not (self.toggle_path)
        self.cur_path_pos: int = 0
        self.bg_color = (
            2 if self.toggle_path
            else 1
        )
        if self.toggle_path and not self.path_displayed:
            self.start_animation()
            self.path_displayed = True
            return None
        self.redraw()

    def change_colors(self) -> None:

        if not self.generated:
            return None

        new_colors: tuple = random.choice(self.color_palette)
        while new_colors == self.current_colors:
            new_colors = random.choice(self.color_palette)
        self.current_colors = new_colors
        self.animating = False
        self.redraw()

    def parse_path(self, path: str) -> list[list]:

        default_path: list[list] = [
            [False for _ in range(len(self.input[0]))]
            for _ in range(len(self.input))
        ]

        if not path:
            return default_path

        row, col = self.coor[0]
        path_to_return: list[list] = default_path
        path_to_return[row][col] = True

        for p in path:

            match p:

                case "N":
                    row -= 1
                case "S":
                    row += 1
                case "W":
                    col -= 1
                case "E":
                    col += 1
                case _:
                    print("Invalid path provided!")
                    return default_path

            if row < 0 or col < 0:
                print("Invalid path provided!")
                return default_path

            path_to_return[row][col] = True

        if (col, row) != self.coor[1]:
            print("Invalid path provided!")
            return default_path

        return path_to_return

    def clear_img(self) -> None:

        self.mlx.mlx_destroy_image(
            self.mlx_ptr,
            self.img
        )
