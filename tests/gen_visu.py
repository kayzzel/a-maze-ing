from src.models import ButtonMenu, MazeGenerator, MazeDisplay, MazeData
from src.utils.events import handle_buttons, handle_keyboard_input
from src.utils.events import global_update
from src.services import parse_config
from mlx import Mlx
import sys


def test_visu() -> None:

    filename: str = "config.txt"

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    maze_data: MazeData | None = parse_config(filename)

    if maze_data is None:
        print("error occured while parsing config file")
        return None

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1920, 1080, "MAZE GENERATION")

    mlx_data: tuple = (mlx, mlx_ptr, mlx_win)

    mlx.mlx_clear_window(mlx_ptr, mlx_win)

    generator: MazeGenerator = MazeGenerator(
        (maze_data.width, maze_data.height),
        maze_data.entry_point,
        maze_data.exit_point,
        maze_data.perfect,
        maze_data.seed
    )

    maze_display: MazeDisplay = MazeDisplay(
        (600, 600),
        (1920, 1080),
        mlx_data
    )

    button_menu: ButtonMenu = ButtonMenu(
        mlx_data,
        maze_display,
        generator,
        (1920, 1080)
    )

    mlx.mlx_mouse_hook(
        mlx_win,
        handle_buttons,
        (
            maze_display,
            button_menu,
            mlx_data
        )
    )
    mlx.mlx_key_hook(
        mlx_win,
        handle_keyboard_input,
        (
            button_menu,
            mlx_data
        )
    )
    mlx.mlx_loop_hook(
        mlx_ptr,
        global_update,
        (maze_display, button_menu, mlx_data)
    )
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":

    test_visu()
