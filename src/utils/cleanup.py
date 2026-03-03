from ..models import Maze


def clear_all(mlx, mlx_ptr, mlx_win, maze: Maze) -> None:

    mlx.mlx_loop_exit(mlx_ptr)
    maze.clear_img()
    mlx.mlx_destroy_window(mlx_ptr, mlx_win)
    mlx.mlx_release(mlx_ptr)
