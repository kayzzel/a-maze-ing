from ...models import Maze, Cell
from .wilson import create_pattern
from random import Random, randint
from enum import Enum
import sys
import resource


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


class GenColor(tuple[int, int, int, int], Enum):

    WALL = (255, 255, 255, 255)
    BG = (0, 0, 0, 255)
    POINT = (255, 0, 0, 255)
    VISITED = (117, 113, 113, 255)
    CURRENT = (0, 255, 0, 255)


def rec_backtrack(
    maze: Maze,
    win_sz: tuple[int, int],
    seed: int | None
) -> None:

    rnd: Random

    if seed is None:

        rnd = Random(randint(0, 10000000000))

    elif isinstance(seed, int) and seed >= 0:

        rnd = Random(seed)

    else:

        raise ValueError("seed must be positive integer")

    entry_point: tuple[int, int] = maze.entry_point
    exit_point: tuple[int, int] = maze.exit_point

    pattern_cells: set[tuple] = create_pattern((maze.width, maze.height))

    visited: list[Cell] = []

    directions: list[str] = list(DIRS.keys())

    sys.setrecursionlimit(10 ** 6)
    resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))

    def backtracking_carving(
        cur_cell: Cell
    ) -> None:

        cur_cell.visited = True

        if cur_cell.coor not in [entry_point, exit_point]:
            cur_cell.bg_color = GenColor.CURRENT

        rnd.shuffle(directions)

        for direction in directions:

            new_x: int = cur_cell.col + DIRS[direction][0]
            new_y: int = cur_cell.row + DIRS[direction][1]

            if is_valid(new_x, new_y, maze, visited, pattern_cells):

                if cur_cell.coor not in [entry_point, exit_point]:
                    cur_cell.bg_color = GenColor.VISITED

                new_cell: Cell = maze.cells[new_y][new_y]
                cur_cell.walls[direction] = False
                new_cell.walls[OPPOSITE[direction]] = False
                backtracking_carving(new_cell)

    maze.start_animation()

    backtracking_carving(
        maze.cells[entry_point[1]][entry_point[0]]
    )

    maze.animating = False
    maze.generated = True


def is_valid(
    x: int,
    y: int,
    maze: Maze,
    visited: list[Cell],
    pattern_cells: set[tuple],
) -> bool:

    return (
        0 <= x < maze.width
        and 0 <= y < maze.height
        and maze.cells[y][x] not in visited
        and (x, y) not in pattern_cells
    )
