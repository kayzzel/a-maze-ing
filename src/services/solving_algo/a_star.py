from ...models import Maze, Cell
import random


WALL_DIRS: dict[str, tuple[int, int]] = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1)
}


class PathCell:
    """
        Description:
    A Cell that containt all the information to solve the maze

        Parameters:
    walls -> contain a bool value for all the wall the keys are the directions
    coor -> the coordinates of the cell (row, col)
    entry_coor -> the coordinate of the start (col, row)
    exit_coor -> the coordinate of the exit (col, row)

        Attributes:
    walls -> the wall (same format as above)
    row -> the row of the cell from the coords
    col -> the col of the cell from the coords
    distance_from_entry -> the distance from the entry in cell count
    distance_from_exit -> an estimation of the distance from the exit using
                          using manhattan formula
    parents -> the PathCell that is the previous from this one
    """
    def __init__(
        self,
        walls: dict[str, bool],
        coor: tuple[int, int],
        entry_coor: tuple[int, int],
        exit_coor: tuple[int, int]
    ) -> None:

        self.walls: dict[str, bool] = walls
        self.row: int
        self.col: int
        self.row, self.col = coor

        self.distance_from_entry: int = 0
        self.distance_from_exit: int = (
            abs(self.row - exit_coor[1])
            + abs(self.col - exit_coor[0])
        )

        self.parent: "PathCell"

    def update(self, parent_cell: "PathCell", in_to_explore: bool) -> None:
        """
            Description:
        update the content of the PathCell

            Parameters:
        parent_cell -> the previous Pathcell
        in_to_explore -> a bool to see if the cell is to be explored
        """

        if (
            not in_to_explore
            or parent_cell.distance_from_entry + 1 < self.distance_from_entry
        ):
            self.distance_from_entry = parent_cell.distance_from_entry + 1
            self.parent = parent_cell


def a_star(
    maze: Maze
) -> str | None:
    """
        Description:
    get a maze and find the shortest path from the entry_point
    to the exit_point using the a_star algorithm with
    a manhattan distance formula

        Parameters:
    maze -> a Maze containing all the information to solve it

        Returns value:
    return the path in a str with the direction as letters (NSEW) to
    the exit from the entry or None if there are no path
    """

    # A list of all the PathCell used to find the exit
    cells: list[list[PathCell]] = []

    # Fill the array with all the PathCells
    for row in range(maze.height):

        # Create an array to store all the PathCells of the row
        cells.append([])

        for col in range(maze.width):

            # Create A PathCell that can be updated later
            cells[row].append(PathCell(
                maze.cells[row][col].walls,
                (row, col),
                maze.entry_point,
                maze.exit_point
            ))

    # Get the PathCell that has the same coordinate as the exit
    cur_cell: PathCell = cells[maze.entry_point[1]][maze.entry_point[0]]

    # Add this PathCell to the explored list
    explored: list[PathCell] = [cur_cell]

    # Find all the valide neighbors of this cell and add the to the list of
    # cells to explore
    to_explore: list[PathCell] = find_valid_neighbors(
        cells,
        cur_cell,
        [],
        explored
    )
    # Reset the solving_steps of the maze and create a list of cells that will
    # be the path
    maze.solving_steps = []
    path_found: list[tuple[int, int]] = []

    # Loop while there is no path found and all the cell has not been explored
    while (
        not path_found
        and len(explored) < maze.height * maze.width
    ):

        # Create a cell that correctop to the current cell
        # to add it in the solving steps
        cell: Cell = Cell(cur_cell.col, cur_cell.row)
        cell.walls = cur_cell.walls
        maze.solving_steps.append(cell)

        # Find the next best Cell to explore
        next_cell: PathCell | None = find_next_cell(to_explore)

        # if no cell is found then end the loop now
        if not next_cell:
            break

        # Remove the cell from the list of the cell that needs to be visited
        # and add it to the one that has been explored
        to_explore.remove(next_cell)
        explored.append(next_cell)

        # if the cell that we got is at the end then create the path
        # and stop the loop here
        if (next_cell.col, next_cell.row) == maze.exit_point:

            path_found = retrace_steps(
                next_cell,
                maze.entry_point
            )
            break

        # Set update the cell that can be explored
        to_explore = find_valid_neighbors(
            cells,
            next_cell,
            to_explore,
            explored
        )

        # Set the cur_cell the next_cell for the next loop
        cur_cell = next_cell

    if not path_found:

        print("Path not found!")
        return None

    # Set the path of the maze to the path found
    maze.path = path_found

    # Get the path composed of cell and translate it to a path of direction
    path_to_return: str | None = compute_path(path_found, maze.entry_point)

    if not path_to_return:
        print("Something went wrong while computing the path")

    # Set the dirs in the maze
    maze.path_dirs = str(path_to_return)

    return path_to_return


def find_valid_neighbors(
    cells: list[list[PathCell]],
    cur_cell: PathCell,
    to_explore: list[PathCell],
    explored: list[PathCell]
) -> list[PathCell]:
    """
        Description:
    Find all reachable neighbors of the current cell and add them to the
    list of cells to explore, updating their distance if a shorter path
    is found

        Parameters:
    cells -> the 2D grid of all PathCells in the maze
    cur_cell -> the PathCell whose neighbors are being examined
    to_explore -> the current list of PathCells waiting to be explored
    explored -> the list of PathCells that have already been visited

        Returns value:
    return the updated to_explore list with any newly found or improved
    neighbors added
    """

    neighbors: list[PathCell] = []

    # Collect all neighbors reachable from cur_cell (i.e. no wall between them)
    for wall, state in cur_cell.walls.items():

        if not state:
            dir_y: int = cur_cell.row + WALL_DIRS[wall][0]
            dir_x: int = cur_cell.col + WALL_DIRS[wall][1]
            neighbors.append(cells[dir_y][dir_x])

    for neighbor in neighbors:

        # Skip neighbors that have already been fully explored
        if neighbor in explored:
            continue

        # Update the neighbor's distance and parent, improving it if possible
        neighbor.update(cur_cell, neighbor in to_explore)

        # Add the neighbor to the exploration list if not already in it
        if neighbor not in to_explore:
            to_explore.append(neighbor)

    return to_explore


def find_next_cell(to_explore: list[PathCell]) -> PathCell | None:
    """
        Description:
    Find the most promising PathCell to explore next by selecting the one
    with the lowest total cost (distance_from_entry + distance_from_exit).
    Ties are broken first by lowest distance_from_exit, then randomly

        Parameters:
    to_explore -> the list of PathCells waiting to be explored

        Returns value:
    return the best PathCell to visit next, or None if to_explore is empty
    """

    if not to_explore:
        return None

    # Sort the cells by their total estimated cost (g + h)
    sorted_list: list[PathCell] = sorted(
        to_explore,
        key=lambda cell: cell.distance_from_entry + cell.distance_from_exit
    )

    # If multiple cells share the lowest total cost, break the tie
    if any(
        (cell.distance_from_entry + cell.distance_from_exit) ==
        (sorted_list[0].distance_from_entry
         + sorted_list[0].distance_from_exit)
        for cell in sorted_list[1:]
    ):

        # Keep only the cells with the lowest total cost
        sorted_list = [
            cell
            for cell in to_explore
            if (cell.distance_from_entry + cell.distance_from_exit) ==
            (sorted_list[0].distance_from_entry
             + sorted_list[0].distance_from_exit)
        ]

        # Among those, sort by distance_from_exit to prefer cell closer to goal
        sorted_list = sorted(
            sorted_list,
            key=lambda cell: cell.distance_from_exit
        )

        # If multiple cells also share the lowest distance_from_exit,
        # pick randomly
        if any(
            cell.distance_from_exit == sorted_list[0].distance_from_exit
            for cell in sorted_list[1:]
        ):

            sorted_list = [
                cell
                for cell in to_explore
                if cell.distance_from_exit == sorted_list[0].distance_from_exit
            ]

            return random.choice(sorted_list)

    return sorted_list[0]


def retrace_steps(
    destination: PathCell,
    entry_coor: tuple[int, int]
) -> list[tuple[int, int]]:
    """
        Description:
    Reconstruct the path from the exit back to the entry by following
    each PathCell's parent until the entry is reached

        Parameters:
    destination -> the PathCell at the exit point of the maze
    entry_coor -> the coordinate of the entry point (col, row)

        Returns value:
    return the path as an ordered list of (col, row) coordinates
    from the entry to the exit (excluding the entry itself)
    """

    cell: PathCell = destination

    path: list[tuple[int, int]] = []

    # Walk backwards from the exit to the entry using parent references
    while (cell.col, cell.row) != entry_coor:

        path.append((cell.col, cell.row))
        cell = cell.parent

    # Reverse the path so it goes from entry to exit
    path.reverse()

    return path


def compute_path(
    path: list[tuple[int, int]],
    entry_coor: tuple[int, int]
) -> str | None:
    """
        Description:
    Convert a list of (col, row) coordinates into a string of cardinal
    directions (N, S, E, W) representing the step-by-step path through
    the maze from the entry point

        Parameters:
    path -> the ordered list of (col, row) coordinates to follow
    entry_coor -> the coordinate of the entry point (col, row)

        Returns value:
    return the path as a string of direction letters (e.g. "NEESW"),
    or None if the path is empty
    """

    cur_row: int
    cur_col: int
    cur_col, cur_row = entry_coor

    directions: str = ""

    for col, row in path:

        # Find which direction leads from the current position to the next cell
        for wall, dirs in WALL_DIRS.items():

            if (
                cur_row == row + dirs[0]
                and cur_col == col + dirs[1]
            ):
                directions += wall

        # Advance the current position to the next cell in the path
        cur_row, cur_col = row, col

    return directions
