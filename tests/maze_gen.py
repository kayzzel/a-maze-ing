from src.models import Maze, Button, generate_buttons
from src.utils import (
    get_color_palette,
    handle_buttons,
    global_update,
    render
)
from mlx import Mlx
import sys


def test_maze_gen() -> None:

    input_filename: str = "tests/input_maze.txt"
    path_name: str = "tests/path.txt"

    if len(sys.argv) < 2:
        print(
            "No input maze file provided - "
            "Resorting to default 'input_maze.txt'"
        )

    else:
        input_filename = sys.argv[1]

    with open(input_filename) as file:
        maze_input: list[str] = [line.rstrip() for line in file]

    with open(path_name) as path_file:
        lines: list[str] = path_file.readlines()
        entry: list[str] = lines[0].rstrip().split(",")
        entry_coor: tuple[int, int] = (int(entry[0]), int(entry[1]))
        exiting: list[str] = lines[1].rstrip().split(",")
        exit_coor: tuple[int, int] = (int(exiting[0]), int(exiting[1]))
        path: str = lines[2].rstrip()

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1920, 1080, "MAZE GENERATION")

    try:
        maze: Maze = Maze(
            maze_input,
            (1920, 1080),
            (600, 600),
            (mlx, mlx_ptr, mlx_win),
            get_color_palette(),
            (path, (entry_coor, exit_coor))
        )
    except ValueError as ve:
        print(ve)
        return None

    buttons: list[Button] = generate_buttons(
        (mlx, mlx_ptr, mlx_win),
        (1920, 1080)
    )

    buttons[0].needs_refresh = True
    render(maze, buttons, (mlx, mlx_ptr, mlx_win))

    mlx.mlx_mouse_hook(
        mlx_win,
        handle_buttons,
        (
            buttons,
            maze,
            (mlx, mlx_ptr, mlx_win)
        )
    )
    mlx.mlx_loop_hook(
        mlx_ptr,
        global_update,
        (maze, buttons, (mlx, mlx_ptr, mlx_win))
    )
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":

    test_maze_gen()
