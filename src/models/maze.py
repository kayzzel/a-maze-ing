from .cell import Cell


class Maze:

    def display_maze(
        self,
        maze_input: list[list[str]],
        maze_sz: tuple[int, int, int],
        mlx_data: tuple
    ) -> None:

        mlx, mlx_ptr, mlx_win = mlx_data

        mlx.mlx_clear_window(mlx_win)

        width, height, px_sz = maze_sz

        maze_img = mlx.mlx_new_image(mlx_ptr, mlx_win, width, height)

        buf, bpp, sz_line, *oth = mlx.mlx_get_img_addr(maze_img)

        for row in range(height):

            for col in range(width):

                cell: Cell = Cell(
                    maze_input[row][col],
                    (col, row),
                    px_sz // width,
                    (buf, sz_line, bpp),
                    (
                        (105, 130, 73, 255),
                        (184, 217, 139, 255)
                    )
                )

                cell.draw()

        mlx.mlx_put_image_to_window(mlx_ptr, mlx_win, maze_img, 0, 0)

        mlx.loop(mlx_ptr)
