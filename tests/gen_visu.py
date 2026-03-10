from src.models import ButtonMenu
from src.utils import handle_buttons, global_update
from src.services import rec_backtrack
from typing import Callable as callable
from mlx import Mlx


def test_visu() -> None:

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1600, 1000, "MAZE GENERATION")

    mlx_data: tuple = (mlx, mlx_ptr, mlx_win)

    mlx.mlx_clear_window(mlx_ptr, mlx_win)

    gen_algo: callable = rec_backtrack

    button_menu: ButtonMenu = ButtonMenu(
        mlx_data,
        gen_algo,
        (1600, 1000)
    )

    mlx.mlx_mouse_hook(
        mlx_win,
        handle_buttons,
        (
            button_menu.maze,
            button_menu,
            mlx_data
        )
    )
    mlx.mlx_loop_hook(
        mlx_ptr,
        global_update,
        (button_menu.maze, button_menu, mlx_data)
    )
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":

    test_visu()
