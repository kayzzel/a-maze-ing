from ..models import Maze, Cell
from .wilson import create_pattern
from random import Random, randint
from enum import Enum


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


class GenColor(Enum):

    WALL = (255, 255, 255, 255)
    BG = (0, 0, 0, 255)
    POINT = (255, 0, 0, 255)
    VISITED = (117, 113, 113, 255)


def rec_backtrack(
    maze_sz: tuple[int, int],
    entry_point: tuple[int, int],
    exit_point: tuple[int, int],
    seed: int | None
) -> Maze:

    maze: Maze = Maze(
        maze_sz,
        entry_point,
        exit_point,
        (
            GenColor.WALL,
            GenColor.BG,
            GenColor.POINT
        )
    )

    rnd: Random

    if seed is None:

        rnd = Random(randint(0, 10000000000))

    elif isinstance(seed, int) and seed >= 0:

        rnd = Random(seed)

    else:

        raise ValueError("seed must be positive integer")

    pattern_cells: set[tuple] = create_pattern(maze_sz)

    visited: list[Cell] = []

    directions: list[str] = list(DIRS.keys())

    def backtracking_carving(
        cur_cell: Cell
    ) -> Maze:

        nonlocal maze
        nonlocal entry_point
        nonlocal exit_point
        nonlocal pattern_cells
        nonlocal visited
        nonlocal directions
        nonlocal rnd

        cur_cell.visited = True

        if cur_cell.coor not in [entry_point, exit_point]:
            cur_cell.bg_color = GenColor.CURRENT

        maze.display_gen_step()

        if cur_cell.coor not in [entry_point, exit_point]:
            cur_cell.bg_color = GenColor.VISITED
            maze.display_gen_step()

        rnd.shuffle(directions)

        for direction in directions:

            new_x: int = cur_cell.col + DIRS[direction][0]
            new_y: int = cur_cell.row + DIRS[direction][1]

            if is_valid(new_x, new_y, maze, visited, pattern_cells):

                new_cell: Cell = maze.cells[new_y][new_y]
                cur_cell.walls[direction] = False
                new_cell.walls[OPPOSITE[direction]] = False
                backtracking_carving(new_cell)

    backtracking_carving(
        maze.cells[entry_point[1]][entry_point[0]]
    )
    return maze


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
