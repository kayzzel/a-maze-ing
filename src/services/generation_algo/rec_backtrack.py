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
    """
        Description:
    Build a maze of the given size using the recursive backtracking algorithm.
    The maze is carved starting from the entry_point and a seed can be provided
    to reproduce the same maze

        Parameters:
    maze_sz -> the size of the maze as (width, height)
    entry_point -> the coordinate of the entry point (col, row)
    exit_point -> the coordinate of the exit point (col, row)
    seed -> an optional positive integer to seed the random generator,
            pass None for a random seed

        Returns value:
    return a fully generated Maze with all walls carved and gen_steps recorded
    """

    rnd: Random

    # Raise the recursion limit to handle large mazes
    # without hitting the default cap
    sys.setrecursionlimit(8000)

    # Set up the random generator, using a random seed if none is provided
    if seed is None:
        rnd = Random(randint(0, 10000000000))
    elif isinstance(seed, int) and seed >= 0:
        rnd = Random(seed)
    else:
        raise ValueError("seed must be positive integer")

    # Raise the limit further now that the seed is validated
    sys.setrecursionlimit(15000)

    # Create the maze and populate its pattern cells before carving
    maze: Maze = Maze(maze_sz, entry_point, exit_point)
    maze.pattern_cells = create_pattern(
            maze.sz, maze.entry_point, maze.exit_point
        )

    # Start carving the maze from the entry cell
    backtracking_carving(
        maze.cells[maze.entry_point[1]][maze.entry_point[0]],
        maze,
        rnd
    )

    return maze


def backtracking_carving(
    cur_cell: Cell,
    maze: Maze,
    rnd: Random
) -> None:
    """
        Description:
    Recursively carve passages through the maze from the current cell using
    the recursive backtracking algorithm. Directions are shuffled at each
    step to ensure a random maze layout

        Parameters:
    cur_cell -> the Cell currently being carved from
    maze -> the Maze being generated, used to access neighbouring cells
    rnd -> the seeded Random instance used to shuffle directions
    """

    # Mark the current cell as visited and record it in the generation steps
    cur_cell.visited = True
    maze.gen_steps.append(cur_cell)

    # Shuffle the directions to carve passages in a random order
    directions: list[str] = list(DIRS.keys())
    rnd.shuffle(directions)

    for direction in directions:

        # Compute the coordinates of the neighbour in this direction
        new_x: int = cur_cell.col + DIRS[direction][0]
        new_y: int = cur_cell.row + DIRS[direction][1]

        if is_valid(new_x, new_y, maze):

            new_cell: Cell = maze.cells[new_y][new_x]

            # Remove the wall between the current cell and the neighbour
            cur_cell.walls[direction] = False
            new_cell.walls[OPPOSITE[direction]] = False

            # Recurse into the neighbour to continue carving
            backtracking_carving(
                new_cell,
                maze,
                rnd
            )

    return None


def is_valid(
    x: int,
    y: int,
    maze: Maze
) -> bool:
    """
        Description:
    Check whether a given coordinate is a valid target to carve into,
    meaning it is within the maze bounds, has not been visited yet,
    and is not part of a reserved pattern cell

        Parameters:
    x -> the column coordinate of the cell to check
    y -> the row coordinate of the cell to check
    maze -> the Maze being generated, used to check bounds and cell states

        Returns value:
    return True if the cell can be carved into, False otherwise
    """

    return (
        0 <= x < maze.width
        and 0 <= y < maze.height
        and not maze.cells[y][x].visited
        and (y, x) not in maze.pattern_cells
    )
