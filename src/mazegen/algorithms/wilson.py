from random import Random, randint
from ...models.maze_generator import Maze
from ...utils.generation_utils import CellCoords, create_pattern

# defines all the directions
DIRECTIONS: list[CellCoords] = [
        (-1, 0),  # North
        (1, 0),   # South
        (0, -1),  # East
        (0, 1),   # West
        ]


def neighbors(
        cell: CellCoords,
        size: tuple[int, int],
        pattern_cells: set[CellCoords]
        ) -> list[CellCoords]:
    """
        Description:
    get a cell and return the list of all it's available neighbors

        Parameters:
    cell -> the coord of the cell that neighbors are returned
    size -> size of the maze in cell (width, height)
    pattern_cells -> set of the cell that are in the pattern

        Return Value:
    list of the cells that are allowed neighbors of a given cell
    (allowed -> in the maze and not in the pattern_cells)
    """

    # unpack the size tuple in height and width
    width: int = size[0]
    height: int = size[1]

    # unpack the cell in row, col
    row, col = cell

    # Initialise the list a the cell neightbors
    neighbors_list: list[CellCoords] = []

    # DIRECTIONS likely contains directions such as:
    # [(1,0), (-1,0), (0,1), (0,-1)]
    for dir_row, dir_col in DIRECTIONS:

        # Compute neighbor coordinates
        new_row, new_col = row + dir_row, col + dir_col
        neighbor: CellCoords = (new_row, new_col)

        # Check the neighbor is inside the grid
        if (0 <= new_row < height and 0 <= new_col < width
                and neighbor not in pattern_cells):

            # Yield the neighbor cell
            neighbors_list.append(neighbor)

    return neighbors_list


def walk(
        cell: CellCoords,
        visited: dict[CellCoords, int],
        unvisited: set[CellCoords],
        path: list[CellCoords],
        size: tuple[int, int],
        pattern_cells: set[CellCoords],
        rnd: Random
        ) -> list[CellCoords]:
    """
        Desciption:
    Perform a random walk until we reach a visited maze cell

        Parameters:
    cell -> coordinate of the starting cell
    visited -> dict of cell contating the coord of the cell as
               a key and its position in the path as the value
    unvisited -> set of the unvisited cells
    path -> list of the cell in the path
    size -> size of the maze in cells (width, height)
    pattern_cells -> set of the cell that are in the pattern
    rnd -> base for the random.choice to be able to use the seed if needed

        Return value:
    return the path, a list of cells from the random cells to the maze
    """

    # Iterate while the path is not connected to the maze
    while cell in unvisited:

        # Choose a random neighboring cell
        # uses the seeded random for the choice
        cell = rnd.choice(neighbors(cell, size, pattern_cells))

        # If we revisit a cell in our current path
        # we found a loop
        if cell in visited:

            # Index where the loop started
            loop: int = visited[cell]

            # Remove the loop by truncating the path
            path = path[:loop+1]

            # Rebuild the visited dictionary
            visited = {
                    cell_coord: index for index, cell_coord in enumerate(path)
                }

        else:
            # Otherwise extend the path
            path.append(cell)

            # Record the position of this cell in the path
            visited[cell] = len(path)-1

    return path


def carve_path(
            maze: Maze,
            path: list[CellCoords],
            unvisited: set[CellCoords],
            unvisited_list: list[CellCoords]
        ) -> None:
    """
        Description:
    Remove the walls of said cells in the maze to carve a given path

        Parameters:
    maze -> The maze that will contain the final maze
    path -> list of the cells that needs to be carved in th maze
    unvisited -> set of all the unvisited cells
    unvisited_list -> list of all the unvisited cells
    """

    # iterate over all the cells of the path to remove the walls
    for index in range(len(path) - 1):

        # unpacking the actual cell
        row, col = path[index]

        # getting the next_cell
        next_cell = path[index + 1]

        # For each cell duo removes the corresponding walls
        # to carve the path in the maze

        # North
        if next_cell == (row - 1, col):
            maze.cells[row][col].walls["N"] = False
            maze.cells[row - 1][col].walls["S"] = False

        # South
        elif next_cell == (row + 1, col):
            maze.cells[row][col].walls["S"] = False
            maze.cells[row + 1][col].walls["N"] = False

        # West
        elif next_cell == (row, col - 1):
            maze.cells[row][col].walls["W"] = False
            maze.cells[row][col - 1].walls["E"] = False

        # East
        elif next_cell == (row, col + 1):
            maze.cells[row][col].walls["E"] = False
            maze.cells[row][col + 1].walls["W"] = False

        # Add the cell to the gen_steps to display the animation
        maze.gen_steps.append(maze.cells[row][col])

        # Add the next_cell to the animation to be sure that it's updated
        maze.gen_steps.append(maze.cells[next_cell[0]][next_cell[1]])

        # Mark the current cell as visited in the maze
        if (row, col) in unvisited:
            unvisited.remove((row, col))
            unvisited_list.remove((row, col))


def wilson(
        size: tuple[int, int],
        entry_point: CellCoords,
        exit_point: CellCoords,
        seed: int | None
        ) -> Maze:
    """
        Description:
    Create a maze of type Maze using the wilson algorithme
    if a seed is given then the maze will use it to generate itself
    so that it can be se same each time with a given seed

        Parameters:
    size -> size of the maze in cells (widthm height)
    entry_point -> start of the maze (x, y)
    exit_point -> exit of the maze (x, y)
    seed -> seed of the maze

        Return value:
    a maze with its size, entry_point, exit_point, cells,
                    step_cells
    """

    # Create a rnd: Random wich is the base form the choices so that:
    rnd: Random

    # Whene no seed is given it generate one randomly
    if seed is None:
        rnd = Random(randint(0, 1000000000))

    # Whene there is a seed given it put the base Random to the seed
    # to be able to generate the same maze with the same seed
    elif isinstance(seed, int) and seed >= 0:
        rnd = Random(seed)

    # When the seed format is wrong it raises a ValueError
    else:
        raise ValueError("seed must be a positive integer")

    # Create a maze with all its informations
    maze: Maze = Maze(size, entry_point, exit_point)

    # unpack the size tuple in height and width
    width: int = size[0]
    height: int = size[1]

    # Getting the cells that form the 42 inside the maze
    pattern_cells: set[CellCoords] = create_pattern(
            size, entry_point, exit_point
        )

    # Saving the cells inside the maze
    maze.pattern_cells = pattern_cells

    # All cells start as unvisited
    unvisited: set[CellCoords] = {
        (row, col)
        for row in range(height)
        for col in range(width)
        if (row, col) not in pattern_cells
    }
    # Creating a list of the cells for more efficient iterating
    unvisited_list: list[CellCoords] = list(unvisited)

    # Pick a random starting cell and mark it visited
    # This becomes the initial tree of the maze
    # uses the seeded random for the choice
    first: CellCoords = rnd.choice(list(unvisited))
    unvisited.remove(first)
    unvisited_list.remove(first)

    # Continue until every cell is added to the maze
    while unvisited:

        # Pick a random unvisited cell to start a random walk
        # uses the seeded random for the choice
        cell: CellCoords = rnd.choice(unvisited_list)

        # Path of the current random walk
        path: list[CellCoords] = [cell]

        # Track visited cells in the current walk
        # value = index of that cell in the path
        visited: dict[CellCoords, int] = {cell: 0}

        # Perform a random walk until we reach a visited maze cell
        path = walk(cell, visited, unvisited, path, size, pattern_cells, rnd)

        # Carve the path into the maze
        carve_path(maze, path, unvisited, unvisited_list)

    # Return the completed maze graph
    return maze
