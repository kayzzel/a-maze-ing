from src.models import Maze
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

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1000, 1000, "MAZE GENERATION")

    maze: Maze = Maze(
        (maze_input, entry_coor, exit_coor),
        (900, 900),
        (mlx, mlx_ptr, mlx_win),
        (
            (0, 0, 255, 255),
            (255, 255, 255, 255),
            (255, 0, 0, 255)
        ),
        path
    )

    maze.display_maze()


if __name__ == "__main__":

    test_maze_gen()
