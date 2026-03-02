from src.models import Maze
from mlx import Mlx
import sys


def test_maze_gen() -> None:

    filename: str = "tests/input_maze.txt"

    if len(sys.argv) != 2:
        print(
            "No input maze file provided - "
            "Resorting to default 'input_maze.txt'"
        )

    else:
        filename = sys.argv[1]

    with open(filename) as file:
        maze_input: list[str] = [line.rstrip() for line in file]

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    mlx_win = mlx.mlx_new_window(mlx_ptr, 1000, 1000, "MAZE GENERATION")

    maze: Maze = Maze(
        maze_input,
        (900, 900),
        (mlx, mlx_ptr, mlx_win),
        []
    )

    maze.display_maze()


if __name__ == "__main__":

    test_maze_gen()
