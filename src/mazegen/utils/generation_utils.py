from random import Random, randint
from src.models.maze_generator import Maze, Cell


# Type alias for a cell's (row, col) coordinate pair
CellCoords = tuple[int, int]


def create_pattern(
        size: tuple[int, int],
        start: CellCoords,
        end: CellCoords
        ) -> set[CellCoords]:
    """
        Description:
    Generate the set of (row, col) coordinates that form the "42" pattern
    centered in the maze. Returns an empty set if the maze is too small
    to fit the pattern or if the entry or exit point overlaps with it

        Parameters:
    size -> the size of the maze as (width, height)
    start -> the (col, row) coordinate of the maze entry point
    end -> the (col, row) coordinate of the maze exit point

        Returns value:
    return a set of (row, col) coordinates forming the pattern,
    or an empty set if the maze is too small or there is a conflict
    with the entry or exit point
    """

    # Unpack the size tuple into width and height
    width, height = size

    # The pattern requires at least a 10x10 maze to fit
    if height < 10 or width < 10:
        return set()

    # Compute the offset needed to center the pattern in the maze
    start_row: int = height // 2 - 2
    start_col: int = width // 2 - 3

    # Define the pattern cells relative to the top-left corner
    pattern_cells: list[CellCoords] = [
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2),    # 4
        (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4),    # 2
        (3, 4), (4, 4), (4, 5), (4, 6)
    ]

    # Shift each pattern cell by the centering offset
    for index in range(len(pattern_cells)):
        new_cell: CellCoords = (
                pattern_cells[index][0] + start_row,
                pattern_cells[index][1] + start_col
                )
        pattern_cells[index] = new_cell

    # Discard the pattern if it would block the entry or exit point
    if start[::-1] in pattern_cells or end[::-1] in pattern_cells:
        return set()

    return set(pattern_cells)


def maze_to_imperfect(
        maze: Maze,
        seed: int | None
        ) -> None:
    """
        Description:
    Introduce loops into a perfect maze by randomly removing one wall
    from cells that currently have three walls closed. Pattern cells and
    out-of-bounds neighbors are never carved into. Each removed wall is
    recorded in gen_steps so the animation reflects the change

        Parameters:
    maze -> the Maze instance to modify in place
    seed -> an optional positive integer to seed the random generator,
            or None for a random seed
    """

    # Build the pattern so imperfect carving avoids those cells
    pattern: set[CellCoords] = create_pattern(
            maze.sz, maze.entry_point, maze.exit_point
        )

    rnd: Random

    # Set up the random generator with the provided or a random seed
    if not seed:
        rnd = Random(randint(0, 1000000000))
    elif isinstance(seed, int) and seed > 0:
        rnd = Random(seed)
    else:
        raise ValueError("Wrong seed format")

    for row in range(maze.height):

        for col in range(maze.width):

            cell: Cell = maze.cells[row][col]

            # Only consider cells with exactly three walls closed (dead ends)
            if len([True for wall in cell.walls.values() if wall]) != 3:
                continue

            # Try to carve north:
            # cell has E, W, N walls and northern neighbor is valid
            if (cell.walls["N"] and cell.walls["W"] and cell.walls["E"] and
                    row - 1 >= 0 and (row - 1, col) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["N"] = False
                maze.gen_steps.append(cell)
                maze.cells[row - 1][col].walls["S"] = False
                maze.gen_steps.append(maze.cells[row - 1][col])

            # Try to carve south:
            # cell has E, W, S walls and southern neighbor is valid
            elif (cell.walls["S"] and cell.walls["W"] and cell.walls["E"] and
                    row + 1 < maze.height and (row + 1, col) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["S"] = False
                maze.gen_steps.append(cell)
                maze.cells[row + 1][col].walls["N"] = False
                maze.gen_steps.append(maze.cells[row + 1][col])

            # Try to carve east:
            # cell has N, S, E walls and eastern neighbor is valid
            elif (cell.walls["E"] and cell.walls["S"] and cell.walls["N"] and
                    col + 1 < maze.width and (row, col + 1) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["E"] = False
                maze.gen_steps.append(cell)
                maze.cells[row][col + 1].walls["W"] = False
                maze.gen_steps.append(maze.cells[row][col + 1])

            # Try to carve west:
            # cell has N, S, W walls and western neighbor is valid
            elif (cell.walls["W"] and cell.walls["S"] and cell.walls["N"] and
                    col - 1 >= 0 and (row, col - 1) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["W"] = False
                maze.gen_steps.append(cell)
                maze.cells[row][col - 1].walls["E"] = False
                maze.gen_steps.append(maze.cells[row][col - 1])
