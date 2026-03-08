from src.models import Maze, ButtonMenu
from src.utils import (
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

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1600, 1000, "MAZE GENERATION")

    try:
        maze: Maze = Maze(
            maze_input,
            (1600, 1000),
            (600, 600),
            (mlx, mlx_ptr, mlx_win),
            [
                (255, 255, 255, 255),
                (0, 0, 0, 255),
                (255, 0, 0, 255),
                (0, 255, 0, 255)
            ],
            (path, (entry_coor, exit_coor))
        )
    except ValueError as ve:
        print(ve)
        return None

    mlx_data: tuple = (mlx, mlx_ptr, mlx_win)
    button_menu: ButtonMenu = ButtonMenu(
        mlx_data,
        maze,
        (1600, 1000)
    )
    button_menu.menus["main"][0].needs_refresh = True
    render(maze, button_menu, mlx_data)

    mlx.mlx_mouse_hook(
        mlx_win,
        handle_buttons,
        (
            button_menu,
            maze,
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

    test_maze_gen()
