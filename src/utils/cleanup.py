"""

clears each byte in the given image byffer by setting it to zero

"""


def clear_img(
    buf: memoryview,
    height: int,
    sz_line: int
) -> None:

    buf[:] = b'\x00' * (height * sz_line)


"""

clears and destroys all the images
then clears and destroys the window
finally exits the mlx loop

"""


def clear_all(mlx_data: tuple, maze, buttons) -> None:

    mlx, mlx_ptr, mlx_win = mlx_data

    maze.clean_img()
    for button in buttons:
        button.clean_img()

    mlx.mlx_clear_window(mlx_ptr, mlx_win)
    mlx.mlx_destroy_window(mlx_ptr, mlx_win)
    mlx.mlx_loop_exit(mlx_ptr)
