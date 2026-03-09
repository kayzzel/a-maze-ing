# steps
#
# Create a new array with the same dimentions as the maze filled with None
# to have the cell already expolered and theyre direction
# 0 -> still; 1 -> North; 2 -> South; 3 -> West; 4 East
#
# Start from the start coordinate
# and set it to True
# create new pathfider for each ways possible
#
# calculate the cost to go to the end (heuristic calcul)
# and add the distance from the start
#
# With the one with the less cost go in the same direction will you can
# (open wall in front and cell not explored)
# and create a new pathfinder at each open wall that is open
# set all the cell that has already been explored at theyre direction
# in the new array
#
# Repeate the 2 previous steps utile the end is found
#
# When the end is found go back to the start using the directions in the array
# for each direction add the letter for the opposite direction
# Reverse the string containing the direction and return it

from src.services.generation_algo.wilson import Cell


def get_path(
        routes: list[list[int]],
        start: Cell,
        end: Cell
        ) -> str:
    # Initialize the path from the start to the end
    path: str = ""

    # Start to create the path from the end to the start with the directions
    cell: Cell = end

    # Loop from the end to the start and add the direction of each cell
    # The next cell is the cell invert of the direction inside the routes
    while (cell != start):
        if routes[cell[0]][cell[1]] == 1:
            cell = (cell[0] - 1, cell[1])
            path += "N"
        elif routes[cell[0]][cell[1]] == 1:
            cell = (cell[0] + 1, cell[1])
            path += "S"
        elif routes[cell[0]][cell[1]] == 1:
            cell = (cell[0], cell[1] - 1)
            path += "W"
        elif routes[cell[0]][cell[1]] == 1:
            cell = (cell[0], cell[1] + 1)
            path += "E"

    return path[::-1]


def create_path_finders(
        maze: list[str],
        cell: Cell,
        path_fiders: list[Cell],
        routes: list[list[int]],
        end: Cell
        ) -> bool:
    # Unpacking the cell into row and coll to have the coordinates
    row, col = cell

    # Converting the value og the cell in the maze in bin to have the walls
    bin_val: str = bin(int(maze[row][col], 16))[2:]
    if not len(bin_val) == 4:
        bin_val = "0" * (4 - len(bin_val)) + bin_val

    # Create the path finders to all the possible directions
    # Add the direction to all the cell where the path finders are
    # Returns True if the path_finder correspond to the end
    if bin_val[3] == "0" and routes[row + 1][col] == -1:
        path_fiders.append((row + 1, col))
        routes[row + 1][col] = 1
        if (row + 1, col) is end:
            return True
    if bin_val[1] == "0" and routes[row - 1][col] == -1:
        path_fiders.append((row - 1, col))
        routes[row - 1][col] = 2
        if (row - 1, col) is end:
            return True
    if bin_val[0] == "0" and routes[row][col - 1] == -1:
        path_fiders.append((row, col - 1))
        routes[row][col - 1] = 3
        if (row, col - 1) is end:
            return True
    if bin_val[2] == "0" and routes[row][col + 1] == -1:
        path_fiders.append((row, col + 1))
        routes[row][col + 1] = 4
        if (row, col + 1) is end:
            return True

    path_fiders.remove(cell)

    return False


def get_path_finder(
        path_finders: list[Cell],
        start: Cell,
        end: Cell
        ) -> Cell:

    path_finder: Cell = path_finders[0]
    path_finder_distance: float = (
            abs(start[0] - path_finder[0]) + abs(start[1] - path_finder[1]) +
            abs(end[0] - path_finder[0]) + abs(end[1] - path_finder[1])
            )

    for next_path_finder in path_finders[1:]:
        next_path_finder_distance: float = (
                abs(start[0] - next_path_finder[0])
                + abs(start[1] - next_path_finder[1]) +
                abs(end[0] - next_path_finder[0])
                + abs(end[1] - next_path_finder[1])
            )

        if next_path_finder_distance < path_finder_distance:
            path_finder = next_path_finder
            path_finder_distance = next_path_finder_distance

    return path_finder


def walk(
        path_finder: Cell,
        maze: list[str],
        path_finders: list[Cell],
        routes: list[list[int]],
        end: Cell
        ) -> bool:
    height: int = len(maze)
    width: int = len(maze[0])

    while True:
        if create_path_finders(maze, path_finder, path_finders, routes, end):
            return True

        if 

    return False


def jump_point_search(
        maze: list[str],
        start: Cell,
        end: Cell,
        ) -> str | None:

    # Get the width and the height from the given maze
    height: int = len(maze)
    width: int = len(maze[0])

    # Create an array that will contain the directions the path finders took
    routes: list[list[int]] = [
            [-1 for _ in range(width)] for _ in range(height)
        ]

    # Create a list af all the path finders
    path_fiders: list[Cell] = []

    # Create all the possible path finders from the start
    routes[start[0]][start[1]] = 0
    if create_path_finders(maze, start, path_fiders, routes, end):
        return get_path(routes, start, end)

    while (path_fiders):

        # a path finder walk into a direction until it can't or
        # it finds the end, the return True if it finds it else False
        if walk(
                get_path_finder(path_fiders, start, end),
                maze, routes, end
                ):
            return get_path(routes, start, end)

    # If no path is found it returns None
    return None
