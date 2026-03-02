from .cell import Cell


class Maze:

    def __init__(
        self,
        maze_input: list[str],
        maze_sz: tuple[int, int],
        mlx_data: tuple,
        colors: tuple,
        path: list[list]
    ) -> None:

        self.input: list[str] = maze_input
        self.width, self.height = maze_sz
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.toggle_path: bool = False
        self.cells: list[list] = []
        self.path: list[list] = path
        self.toggle_path: bool = True
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

        for row in range(len(self.input)):

            self.cells.append([])

            for col in range(len(self.input[0])):

                bg_color: int = 1

                if self.toggle_path and self.path[row][col]:
                    bg_color = 2

                self.cells[row].append(Cell(
                    self.input[row][col],
                    (col, row),
                    self.width // len(self.input[0]),
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

    def toggle_path(self) -> None:

        self.toggle_path = True
        self.draw()

    def change_colors(self, new_colors: tuple) -> None:

        self.colors = new_colors
        self.draw()
