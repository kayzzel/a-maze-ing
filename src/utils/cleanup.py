def clear_img(buf: memoryview) -> None:

    buf[:] = b"\x00" * len(buf)


def clear_all(mlx, mlx_ptr, mlx_win, maze, buttons) -> None:

    maze.clean_img()
    for button in buttons:
        button.clean_img()
    mlx.mlx_clear_window(mlx_ptr, mlx_win)
    mlx.mlx_destroy_window(mlx_ptr, mlx_win)
    mlx.mlx_loop_exit(mlx_ptr)
