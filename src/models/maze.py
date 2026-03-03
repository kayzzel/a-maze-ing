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
        self.path: list[list] = self.parse_path(path[0])
        self.coor: tuple = path[1]
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
        self.maze_pos: tuple = maze_pos

    def display_maze(self) -> None:

        clear_img(self.buf)
        cells: list[list] = []

        for row in range(len(self.input)):

            cells.append([])

            for col in range(len(self.input[0])):

                bg_color: int = 1

                if self.toggle_path and self.path[row][col]:
                    bg_color = 2

                cells[row].append(Cell(
                    self.input[row][col],
                    (col, row),
                    self.width // len(self.input[0]),
                    (self.buf, self.sz_line, self.bpp),
                    (
                        self.current_colors[0],
                        self.current_colors[bg_color]
                    )
                ))

                cells[row][col].draw()

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.maze_pos
        )

    def toggle_path_on_off(self) -> None:

        self.toggle_path = not (self.toggle_path)
        self.display_maze()

    def change_colors(self) -> None:

        new_colors: tuple = random.choice(self.color_palette)
        while new_colors == self.current_colors:
            new_colors = random.choice(self.color_palette)
        self.current_colors = new_colors
        self.display_maze()

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
