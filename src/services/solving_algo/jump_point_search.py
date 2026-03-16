from ...models.maze_generator import Maze
from src.utils.generation_utils import CellCoords


def get_path(
        maze: Maze,
        routes: list[list[int]],
        ) -> str:
    """
        Description:
    create the route from the start to the exit using the directions
    the path_finders made in the maze

        Parameters:
    maze -> the maze with all the cells and infos
    routes -> a list of all the direction the path_finders took

        Returns value:
    a string of the directions from the start to the end (NWSE)
    """

    # Get the start and exit from the maze
    start: CellCoords = maze.entry_point
    end: CellCoords = maze.exit_point

    # Reset the path inside the maze
    maze.path = []

    # Initialize the reverse path from the start to the end
    path: str = ""

    # Start to create the path from the end to the start with the directions
    cell: CellCoords = end[::-1]

    # Loop from the end to the start and add the direction of each cell
    # The next cell is the cell invert of the direction inside the routes
    while (cell != start[::-1]):
        if routes[cell[0]][cell[1]] == 1:
            cell = (cell[0] + 1, cell[1])
            path += "N"
        elif routes[cell[0]][cell[1]] == 2:
            cell = (cell[0] - 1, cell[1])
            path += "S"
        elif routes[cell[0]][cell[1]] == 3:
            cell = (cell[0], cell[1] + 1)
            path += "W"
        elif routes[cell[0]][cell[1]] == 4:
            cell = (cell[0], cell[1] - 1)
            path += "E"
        else:
            raise Exception("Error while parsing the Maze")
        maze.path.append(cell[::-1])

    maze.path = maze.path[-2::-1]
    maze.path_dirs = path[::-1]
    # return the reverse path into the right order
    return path[::-1]


def create_path_finders(
        maze: Maze,
        cell: CellCoords,
        path_finders: set[CellCoords],
        routes: list[list[int]],
        ) -> bool:
    """
        Description:
    create path_finder to all the open directions

        Parameters:
    maze -> the maze with all the cells and infos
    cell -> the coordinates of the cell we have to create path_finders around
    path_finders -> list of all the path_finders
    routes -> a list of all the direction the path_finders took

        Returns value:
    a bool that is True if the end has been found during the walk else False
    """

    # Get the coordinate from the exit in the maze
    end: CellCoords = maze.exit_point

    # Unpacking the cell into row and col to have the coordinates
    row, col = cell

    # Converting the value of the cell in the maze in bin to have the walls
    walls: dict[str, bool] = maze.cells[row][col].walls

    # Create the path finders to all the possible directions
    # Add the direction to all the cells where the path finders are
    # Returns True if the path_finder corresponds to the end

    # North
    if not walls["N"] and routes[row - 1][col] == -1:
        path_finders.add((row - 1, col))
        routes[row - 1][col] = 1
        maze.solving_steps.append(maze.cells[row - 1][col])
        if (col, row - 1) == end:
            return True

    # South
    if not walls["S"] and routes[row + 1][col] == -1:
        path_finders.add((row + 1, col))
        routes[row + 1][col] = 2
        maze.solving_steps.append(maze.cells[row + 1][col])
        if (col, row + 1) == end:
            return True

    # West
    if not walls["W"] and routes[row][col - 1] == -1:
        path_finders.add((row, col - 1))
        routes[row][col - 1] = 3
        maze.solving_steps.append(maze.cells[row][col - 1])
        if (col - 1, row) == end:
            return True

    # East
    if not walls["E"] and routes[row][col + 1] == -1:
        path_finders.add((row, col + 1))
        routes[row][col + 1] = 4
        maze.solving_steps.append(maze.cells[row][col + 1])
        if (col + 1, row) == end:
            return True

    path_finders.remove(cell)

    return False


def get_path_finder(
        path_finders: list[CellCoords],
        start: CellCoords,
        end: CellCoords
        ) -> CellCoords:
    """
        Description:
    calculate the distance of all the path_finder from the start + the end
    using the manhattan distance formula
    and return the one with the sortest distance

        Parameters:
    path_finder -> list of all the path_finders
    start -> coordinate of the start (x, y)
    end -> coordinate of the exit(x, y)

        Returns value:
    return the coordinates of the path_finders with the shortest distance
    """
    # unpack the start and the exit into their coordinates
    sx, sy = start
    ex, ey = end

    # get the first path_finder in the array and unpack its coordinates
    path_finder = path_finders[0]
    x, y = path_finder

    # calculate the distance from the start + the end
    # with the manhattan distance formula
    path_finder_distance = (
            abs(sx - x) + abs(sy - y) + abs(ex - x) + abs(ey - y)
        )

    # loops for all the path_finders
    for i in range(1, len(path_finders)):

        # get the coordinates of the next path_finder
        x, y = path_finders[i]

        # calculate its distance using the same formula as before
        next_distance = abs(sx - x) + abs(sy - y) + abs(ex - x) + abs(ey - y)

        # test if it is nearer than the previous nearest one
        # if that is the case store the new best path_finder
        # and its distance
        if next_distance < path_finder_distance:
            path_finder = (x, y)
            path_finder_distance = next_distance

    # Return the nearest path_finder
    return path_finder


def walk(
        path_finder: CellCoords,
        maze: Maze,
        path_finders: set[CellCoords],
        routes: list[list[int]],
        ) -> bool:
    """
        Description:
    walk into the same direction until it is blocked or it find the exit
    create path finder at each intersection

        Parameters:
    path_finder -> the coord of the best path_finder found
    maze -> the maze
    path_finders -> set of all the path_finders
    routes -> list the directions

        Return value:
    a bool that is True if the end has been found during the walk else False
    """

    # loop while there still are path finders in the maze
    while (path_finders):

        # Unpack the path_finder to get its coordinates
        row, col = path_finder

        # Get the direction the current path_finder goes to
        direction = routes[row][col]

        # Create the coord for the next path_finder in the same direction
        next_row, next_col = row, col

        # add or remove on to the coord to have the coord of the next case
        # in the good direction
        if direction == 1:  # North
            next_row -= 1
        elif direction == 2:  # South
            next_row += 1
        elif direction == 3:  # West
            next_col -= 1
        elif direction == 4:  # East
            next_col += 1
        # If the direction is not set raise an error
        elif direction != 0:
            raise Exception("Error while parsing the Maze")

        # Create new path_finder
        # if one of the new path_finder is on the exit return True
        if create_path_finders(maze, path_finder, path_finders, routes):
            return True

        # Test if there is a new path_finder in the same direction that
        # the actual one goes to, if that is the case set the actual
        # path_finder to the new coord and continue the loop
        if ((next_row, next_col) in path_finders and
                routes[next_row][next_col] == direction):
            path_finder = (next_row, next_col)

        # If that is not the case return false to continue and calculate
        # the new best path_finder
        else:
            return False

    return False


def jump_point_search(
        maze: Maze
        ) -> str | None:
    """
        Description:
    get a maze and find the shortest path from the entry_point
    to the exit_point using the jump_point_search algorithm with
    a manhattan distance algorithm

        Parameters:
    maze -> a maze containing all the relevant information
            that are needed to solve it

        Return Value:
    return the string of the direction from the start to the exit
    if there is a path else return None
    """

    # Get the start and exit from the given maze
    start: CellCoords = maze.entry_point
    end: CellCoords = maze.exit_point

    # Reseting the solving steps in case there already are some in
    maze.solving_steps = []

    # Returns an empty path if the entry and exit are the same cell
    if start == end:
        maze.path_dirs = ""
        maze.path = []
        return ""

    # Get the width and height from the given maze
    height: int = maze.height
    width: int = maze.width

    # Create an array that will contain the directions the path finders took
    routes: list[list[int]] = [
            [-1 for _ in range(width)] for _ in range(height)
        ]

    # Create a list af all the path finders
    path_finders: set[CellCoords] = {(start[1], start[0])}

    # Create all the possible path finders from the start
    routes[start[1]][start[0]] = 0

    # loop while there still are path finders in the maze
    while (path_finders):

        # a path finder walks into a direction until it can't or
        # it finds the end, then return True if it finds it else False
        if walk(
                get_path_finder(list(path_finders), start, end),
                maze, path_finders,  routes
                ):
            # take the array with the direction and
            # Go from the exit to the start using the inverted direction
            # Then return the path that it used to make it
            return get_path(maze, routes)

    # If no path is found it returns None
    return None
