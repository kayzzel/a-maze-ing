# steps
#
# Create a new array with the same dimensions as the maze filled with None
# to have the cell already explored and its direction
# 0 -> still; 1 -> North; 2 -> South; 3 -> West; 4 -> East
#
# Start from the start coordinates
# and set it to True
# create new pathfinder for each way possible
#
# calculate the cost to go to the end (heuristic calcul)
# and add the distance from the start
#
# With the one with the less cost go in the same direction while you can
# (open wall in front and cell not explored)
# and create a new pathfinder at each wall that is open
# set all the cells that have already been explored at their direction
# in the new array
#
# Repeat the 2 previous steps until the end is found
#
# When the end is found go back to the start using the directions in the array
# for each direction add the letter for the opposite direction
# Reverse the string containing the direction and return it

from src.services.generation_algo.wilson import Cell as CellCoords


class Cell:

    def __init__(
        self,
        x: int,
        y: int
    ) -> None:

        self.row: int = y
        self.col: int = x
        self.coor: tuple[int, int] = (x, y)
        self.walls: dict[str, bool] = {
            "N": True,
            "S": True,
            "W": True,
            "E": True
        }
        self.visited: bool = False


class Maze:

    def __init__(
        self,
        size: tuple[int, int],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int]
    ) -> None:

        self.sz: tuple[int, int] = size
        self.width: int = self.sz[0]
        self.height: int = self.sz[1]

        self.entry_point: tuple[int, int] = entry_point
        self.exit_point: tuple[int, int] = exit_point

        self.cells: list[list[Cell]] = [
            [
                Cell(col, row)
                for col in range(self.width)
            ]
            for row in range(self.height)
        ]

        self.gen_steps: list[Cell] = []
        self.solving_steps: list[Cell] = []

        self.path: list[tuple]
        self.path_dirs: str

    def maze_to_hexa(self) -> list[str]:

        walls_values: dict[str, int] = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8
        }

        hexa_maze: list[str] = [
            "" for _ in range(len(self.cells))
        ]

        for row in range(len(self.cells)):

            for cell in self.cells[row]:

                val: int = 0

                for wall, state in cell.walls.items():

                    if state:
                        val |= walls_values[wall]

                hexa_maze[row] += ("0123456789ABCDEF")[val]

        return hexa_maze


def get_path(
        maze: Maze,
        routes: list[list[int]],
        ) -> str:

    start: CellCoords = maze.entry_point
    end: CellCoords = maze.exit_point

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

    start: CellCoords = maze.entry_point
    end: CellCoords = maze.exit_point

    maze.solving_steps = []

    # Returns an empty path if the entry and exit are the same cell
    if start == end:
        return ""

    # Get the width and the height from the given maze
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
