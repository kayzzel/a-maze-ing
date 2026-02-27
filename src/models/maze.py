from .cell import Cell


class Maze:

    @staticmethod
    def display_maze(
        maze_input: list[str],
        maze_sz: tuple[int, int],
        mlx_data: tuple
    ) -> None:

        mlx, mlx_ptr, mlx_win = mlx_data

        mlx.mlx_clear_window(mlx_ptr, mlx_win)

        width, height = maze_sz

        maze_img = mlx.mlx_new_image(mlx_ptr, width, height)

        buf, bpp, sz_line, *oth = mlx.mlx_get_data_addr(maze_img)

        for row in range(len(maze_input)):

            for col in range(len(maze_input[0])):

                cell: Cell = Cell(
                    maze_input[row][col],
                    (col, row),
                    width // len(maze_input[0]),
                    (buf, sz_line, bpp),
                    (
                        (105, 130, 73, 255),
                        (184, 217, 139, 255)
                    )
                )

                cell.draw()

        mlx.mlx_put_image_to_window(mlx_ptr, mlx_win, maze_img, 100, 100)

        mlx.mlx_loop(mlx_ptr)
