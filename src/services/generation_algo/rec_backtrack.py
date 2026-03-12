from ...models.maze_generator import Maze, Cell
from src.utils.generation_utils import create_pattern
from random import Random, randint
import sys


DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}


OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}


def rec_backtrack(
    maze_sz: tuple[int, int],
    entry_point: tuple[int, int],
    exit_point: tuple[int, int],
    seed: int | None
) -> Maze:

    rnd: Random

    sys.setrecursionlimit(8000)

    if seed is None:

        rnd = Random(randint(0, 10000000000))

    elif isinstance(seed, int) and seed >= 0:

        rnd = Random(seed)

    else:

        raise ValueError("seed must be positive integer")

    sys.setrecursionlimit(8000)

    maze: Maze = Maze(maze_sz, entry_point, exit_point)

    pattern_cells: set[tuple] = create_pattern(
            maze.sz, maze.entry_point, maze.exit_point
        )

    backtracking_carving(
        maze.cells[maze.entry_point[1]][maze.entry_point[0]],
        maze,
        rnd,
        pattern_cells
    )

    return maze


def backtracking_carving(
    cur_cell: Cell,
    maze: Maze,
    rnd: Random,
    pattern_cells: set[tuple]
) -> None:

    cur_cell.visited = True

    """
    saved_step: Cell = Cell(
        cur_cell.col,
        cur_cell.row
    )
    # saved_step.visited = True
    saved_step.walls = cur_cell.walls
    """

    maze.gen_steps.append(cur_cell)

    directions: list[str] = list(DIRS.keys())

    rnd.shuffle(directions)

    for direction in directions:

        new_x: int = cur_cell.col + DIRS[direction][0]
        new_y: int = cur_cell.row + DIRS[direction][1]

        if is_valid(new_x, new_y, maze, pattern_cells):

            new_cell: Cell = maze.cells[new_y][new_x]
            cur_cell.walls[direction] = False
            new_cell.walls[OPPOSITE[direction]] = False
            backtracking_carving(
                new_cell,
                maze,
                rnd,
                pattern_cells
            )

    return None


def is_valid(
    x: int,
    y: int,
    maze: Maze,
    pattern_cells: set[tuple]
) -> bool:

    return (
        0 <= x < maze.width
        and 0 <= y < maze.height
        and not maze.cells[y][x].visited
        and (y, x) not in pattern_cells
    )
