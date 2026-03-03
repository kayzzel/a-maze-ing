from random import choice
from typing import Generator


# define the type of a cell
Cell = tuple[int, int]

# defines all the directions
DIRS: list[Cell] = [
        (-1, 0),  # North
        (1, 0),   # South
        (0, -1),  # East
        (0, 1),   # West
        ]


# Return all valid neighboring cells of a given cell
def neighbors(
        cell: Cell,
        size: tuple[int, int]
      ) -> Generator[Cell, None, None]:

    # unpack the size tuple in height and width
    height: int
    width: int
    height, width = size

    row: int
    col: int
    row, col = cell

    # DIRS likely contains directions such as:
    # [(1,0), (-1,0), (0,1), (0,-1)]
    for dir_row, dir_col in DIRS:

        # Compute neighbor coordinates
        new_row, new_col = row + dir_row, col + dir_col

        # Check the neighbor is inside the grid
        if 0 <= new_row < height and 0 <= new_col < width:

            # Yield the neighbor cell
            yield (new_row, new_col)


def walk(
        cell: Cell,
        visited: dict[Cell, int],
        unvisited: set[Cell],
        path: list[Cell],
        size: tuple[int, int]
        ) -> list[Cell]:
    """
    Perform a random walk until we reach a visited maze cell
    """
    while cell in unvisited:

        # Choose a random neighboring cell
        cell = choice(list(neighbors(cell, size)))

        # If we revisit a cell in our current path
        # we found a loop
        if cell in visited:

            # Index where the loop started
            loop: int = visited[cell]

            # Remove the loop by truncating the path
            path = path[:loop+1]

            # Rebuild the visited dictionary
            visited = {p: i for i, p in enumerate(path)}

        else:
            # Otherwise extend the path
            path.append(cell)

            # Record the position of this cell in the path
            visited[cell] = len(path)-1

    return path


def wilson(size: tuple[int, int]) -> list[str]:

    # unpack the size tuple in height and width
    height: int
    width: int
    height, width = size

    # Maze representation:
    # Each cell maps to a set of cells it is connected to
    maze: dict[Cell, set[Cell]] = {
        (row, col): set() for row in range(height) for col in range(width)
    }

    # All cells start as unvisited
    unvisited: set[Cell] = set(maze.keys())

    # Pick a random starting cell and mark it visited
    # This becomes the initial tree of the maze
    first: Cell = choice(list(unvisited))
    unvisited.remove(first)

    # Continue until every cell is added to the maze
    while unvisited:

        # Pick a random unvisited cell to start a random walk
        cell: Cell = choice(list(unvisited))

        # Path of the current random walk
        path: list[Cell] = [cell]

        # Track visited cells in the current walk
        # value = index of that cell in the path
        visited: dict[Cell, int] = {cell: 0}

        # Perform a random walk until we reach a visited maze cell
        path = walk(cell, visited, unvisited, path, size)

        # Carve the path into the maze
        for index in range(len(path) - 1):

            current_cell = path[index]
            next_cell = path[index + 1]

            # Create a bidirectional connection between the two cells
            maze[current_cell].add(next_cell)
            maze[next_cell].add(current_cell)

            # Mark the current cell as visited in the maze
            if current_cell in unvisited:
                unvisited.remove(current_cell)

    # Return the completed maze graph
    return maze_to_hexa(maze, size)


def maze_to_hexa(
        maze: dict[Cell, set[Cell]],
        size: tuple[int, int]
        ) -> list[str]:
    """
    Convert a maze represented as adjacency lists into a hexadecimal grid.

    Each cell is encoded with one hex digit describing which walls are closed:
        bit 0 (1) -> North wall closed
        bit 1 (2) -> East wall closed
        bit 2 (4) -> South wall closed
        bit 3 (8) -> West wall closed

    Result a list of strings, where each character corresponds to one cell.
    """

    def cell_to_hexa(cell: Cell, links: set[Cell]) -> str:
        """
        Compute the hexadecimal encoding for a single cell.

        `links` contains all neighboring cells connected to `cell`.
        If a neighbor in a direction is NOT in links, the wall is closed.
        """

        row: int
        col: int
        row, col = cell

        # Bitmask value representing closed walls
        value: int = 0

        # Directions with their corresponding bit values
        directions = [
            ((-1, 0), 1),  # North
            ((0, 1), 2),   # East
            ((1, 0), 4),   # South
            ((0, -1), 8),  # West
        ]

        # Check each direction to see if the wall is closed
        for (dir_row, dir_col), bit in directions:

            # If the neighbor is not connected, the wall is closed
            if (row + dir_row, col + dir_col) not in links:
                value |= bit

        # Convert the bitmask to a hexadecimal character
        return hex(value)[2:]

    # unpack the size tuple in height and width
    height: int
    width: int
    height, width = size

    # Initialize the resulting maze as a list of strings (one per row)
    maze_hexa: list[str] = ["" for _ in range(height)]

    # Iterate over every cell in the grid
    for row in range(height):
        for col in range(width):

            cell: Cell = (row, col)

            # Cells connected to this one (open passages)
            nexts: set[Cell] = maze[cell]

            # Append the hexadecimal encoding of the cell
            maze_hexa[row] += cell_to_hexa(cell, nexts)

    return maze_hexa
