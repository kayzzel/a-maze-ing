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

    neighbors: list[PathCell] = []

    for wall, state in cur_cell.walls.items():

        if not state:
            dir_y: int = cur_cell.row + WALL_DIRS[wall][0]
            dir_x: int = cur_cell.col + WALL_DIRS[wall][1]
            neighbors.append(cells[dir_y][dir_x])

    for neighbor in neighbors:

        if neighbor in explored:
            continue

        neighbor.update(cur_cell, neighbor in to_explore)

        if neighbor not in to_explore:
            to_explore.append(neighbor)

    return to_explore


def find_next_cell(to_explore: list[PathCell]) -> PathCell | None:

    if not to_explore:
        return None

    sorted_list: list[PathCell] = sorted(
        to_explore,
        key=lambda cell: cell.distance_from_entry + cell.distance_from_exit
    )

    if any(
        (cell.distance_from_entry + cell.distance_from_exit) ==
        (sorted_list[0].distance_from_entry
         + sorted_list[0].distance_from_exit)
        for cell in sorted_list[1:]
    ):

        sorted_list = [
            cell
            for cell in to_explore
            if (cell.distance_from_entry + cell.distance_from_exit) ==
            (sorted_list[0].distance_from_entry
             + sorted_list[0].distance_from_exit)
        ]

        sorted_list = sorted(
            sorted_list,
            key=lambda cell: cell.distance_from_exit
        )

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

    cell: PathCell = destination

    path: list[tuple[int, int]] = []

    while (cell.col, cell.row) != entry_coor:

        path.append((cell.col, cell.row))
        cell = cell.parent

    path.reverse()

    return path


def compute_path(
    path: list[tuple[int, int]],
    entry_coor: tuple[int, int]
) -> str | None:

    cur_row: int
    cur_col: int
    cur_col, cur_row = entry_coor

    directions: str = ""

    for col, row in path:

        for wall, dirs in WALL_DIRS.items():

            if (
                cur_row == row + dirs[0]
                and cur_col == col + dirs[1]
            ):
                directions += wall

        cur_row, cur_col = row, col

    return directions
