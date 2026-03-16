from typing import Any as any


def clear_img(
    buf: memoryview,
    height: int,
    sz_line: int
) -> None:
    """
        Description:
    Clear an MLX image buffer by zeroing every byte it contains

        Parameters:
    buf -> the memoryview of the image buffer to clear
    height -> the height of the image in pixels
    sz_line -> the number of bytes per row in the buffer
    """

    buf[:] = b'\x00' * (height * sz_line)


def clear_all(mlx_data: tuple, maze: any) -> None:
    """
        Description:
    Perform a full cleanup before closing the application. Clears and
    destroys all maze images, clears and destroys the window, then
    exits the MLX loop

        Parameters:
    mlx_data -> a tuple containing (mlx, mlx_ptr, mlx_win) for the MLX instance
    maze -> the MazeDisplay instance whose images need to be cleaned up
    """

    mlx, mlx_ptr, mlx_win = mlx_data

    # Clean up all maze images first
    maze.clean_img()

    # Clear and destroy the window, then exit the loop
    mlx.mlx_clear_window(mlx_ptr, mlx_win)
    mlx.mlx_destroy_window(mlx_ptr, mlx_win)
    mlx.mlx_loop_exit(mlx_ptr)
