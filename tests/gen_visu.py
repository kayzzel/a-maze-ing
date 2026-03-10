from src.models import ButtonMenu, Maze
from src.utils import handle_buttons, global_update
from mlx import Mlx


def test_visu() -> None:

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1600, 1000, "MAZE GENERATION")

    mlx_data: tuple = (mlx, mlx_ptr, mlx_win)

    mlx.mlx_clear_window(mlx_ptr, mlx_win)

    maze: Maze = Maze(
        (25, 20),
        (1600, 1000),
        mlx_data,
        (1, 1),
        (19, 14)
    )

    button_menu: ButtonMenu = ButtonMenu(
        mlx_data,
        maze,
        (1600, 1000)
    )

    mlx.mlx_mouse_hook(
        mlx_win,
        handle_buttons,
        (
            maze,
            button_menu,
            mlx_data
        )
    )
    mlx.mlx_loop_hook(
        mlx_ptr,
        global_update,
        (maze, button_menu, mlx_data)
    )
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":

    test_visu()
