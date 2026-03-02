from .cell import Cell


class Maze:

    def __init__(
        self,
        maze_input: list[str],
        maze_sz: tuple[int, int],
        mlx_data: tuple,
        path: list[list]
    ) -> None:

        self.input: list[str] = maze_input
        self.maze_sz: tuple[int, int] = maze_sz
        self.mlx_data: tuple = mlx_data
        self.toggle_path: bool = False
        self.cells: list[list] = []
        self.path: list[list] = path
        self.toggle_path: bool = True

    def display_maze(self) -> None:

        mlx, mlx_ptr, mlx_win = self.mlx_data

        mlx.mlx_clear_window(mlx_ptr, mlx_win)

        width, height = self.maze_sz

        self.img = mlx.mlx_new_image(mlx_ptr, width, height)

        buf, bpp, sz_line, *oth = mlx.mlx_get_data_addr(self.img)

        colors: tuple[tuple] = (
            (105, 130, 73, 255),
            (184, 217, 139, 255)
        )

        for row in range(len(self.maze_input)):

            self.cells.append([])

            for col in range(len(self.maze_input[0])):

                if self.toggle_path and self.path[row][col]:
                    colors[1] = (255, 0, 0, 255)

                self.cells[row].append(Cell(
                    self.maze_input[row][col],
                    (col, row),
                    width // len(self.maze_input[0]),
                    (buf, sz_line, bpp),
                    colors
                ))

                self.cells[row][col].draw()

        mlx.mlx_put_image_to_window(mlx_ptr, mlx_win, maze_img, 100, 100)

        mlx.mlx_loop(mlx_ptr)

    def toggle_path(self) -> None:

        self.toggle_path = True
        self.draw()
