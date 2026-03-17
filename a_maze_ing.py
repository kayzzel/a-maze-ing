from src.models import ButtonMenu, MazeDisplay, MazeData
from src.mazegen import MazeGenerator
from src.utils.events import handle_buttons, handle_keyboard_input
from src.utils.events import global_update
from src.utils.cleanup import clear_all
from src.services import parse_config
from mlx import Mlx
import sys


def main() -> None:

    filename: str = "config.txt"

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print(
                "No configuration filename provided - "
                "Resorting to default 'config.txt'.\n"
                "To use your own parameters,"
                "run 'python3 a_maze_ing.py <filename>"
                )

    maze_data: MazeData | None = parse_config(filename)

    if maze_data is None:
        print("Error occured while parsing config file")
        return None

    try:
        generator: MazeGenerator = MazeGenerator(
            (maze_data.width, maze_data.height),
            maze_data.entry_point,
            maze_data.exit_point,
            maze_data.perfect,
            maze_data.seed
        )
    except ValueError as ve:
        print(ve)
        return None

    if not generator.write_to_output(
        generator.generate_maze(),
        maze_data.output_filename
    ):
        return None

    import tkinter as tk

    root = tk.Tk()
    root.withdraw()

    width: int = root.winfo_screenwidth()
    height: int = root.winfo_screenheight()

    root.destroy()

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    mlx_win = mlx.mlx_new_window(mlx_ptr, width, height, "A-MAZE-ING")

    mlx_data: tuple = (mlx, mlx_ptr, mlx_win)

    mlx.mlx_clear_window(mlx_ptr, mlx_win)

    maze_display: MazeDisplay = MazeDisplay(
        ((height // 10) * 6, (height // 10) * 6),
        (width, height),
        mlx_data
    )

    button_menu: ButtonMenu = ButtonMenu(
        mlx_data,
        maze_display,
        generator,
        (width, height)
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
    clear_all(
       mlx_data,
       button_menu
    )


if __name__ == "__main__":

    main()
