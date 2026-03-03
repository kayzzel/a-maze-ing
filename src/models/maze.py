from .cell import Cell
# import time


class Maze:

    def __init__(
        self,
        maze_input: tuple,
        maze_sz: tuple[int, int],
        mlx_data: tuple,
        colors: tuple,
        path: str
    ) -> None:

        self.grid, *self.coor = maze_input
        self.width, self.height = maze_sz
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.toggle_path: bool = False
        self.cells: list[list] = []
        self.path: list[list] = self.parse_path(path)
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )
        self.buf, self.bpp, self.sz_line, *oth = (
            self.mlx.mlx_get_data_addr(self.img)
        )
        self.colors: tuple = colors

    def display_maze(self) -> None:

        self.mlx.mlx_clear_window(self.mlx_ptr, self.mlx_win)

        for row in range(len(self.grid)):

            self.cells.append([])

            for col in range(len(self.grid[0])):

                bg_color: int = 1

                if self.toggle_path and self.path[row][col]:
                    bg_color = 2

                self.cells[row].append(Cell(
                    self.grid[row][col],
                    (col, row),
                    self.width // len(self.grid[0]),
                    (self.buf, self.sz_line, self.bpp),
                    (self.colors[0], self.colors[bg_color])
                ))

                self.cells[row][col].draw()

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            100,
            100
        )

        self.mlx.mlx_loop(self.mlx_ptr)

    def toggle_path_on_off(self, on_off: bool) -> None:

        self.toggle_path = on_off
        self.display_maze()

    def change_colors(self, new_colors: tuple) -> None:

        self.colors = new_colors
        self.draw()

    def parse_path(self, path: str) -> list[list]:

        default_path: list[list] = [
            [False for _ in range(len(self.grid[0]))]
            for _ in range(len(self.grid))
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
