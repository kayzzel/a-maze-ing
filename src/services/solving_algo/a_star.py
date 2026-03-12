from ...models import Maze
import random


WALL_DIRS: dict[str, tuple[int, int]] = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1)
}


class PathCell:

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
    if not check_maze_input(maze_input):
        print("Invalid maze input!")
        return None
    """

    cells: list[list[PathCell]] = []

    for row in range(maze.height):

        cells.append([])

        for col in range(maze.width):

            cells[row].append(PathCell(
                maze.cells[row][col].walls,
                (row, col),
                maze.entry_point,
                maze.exit_point
            ))

    cur_cell: PathCell = cells[maze.entry_point[1]][maze.entry_point[0]]
    explored: list[PathCell] = [cur_cell]
    to_explore: list[PathCell] = find_valid_neighbors(
        cells,
        cur_cell,
        [],
        explored
    )
    maze.solving_steps = []
    path_found: list[tuple[int, int]] = []

    while (
        not path_found
        and len(explored) < maze.height * maze.width
    ):

        maze.solving_steps.append(cur_cell)

        next_cell: PathCell | None = find_next_cell(to_explore)

        if not next_cell:
            break

        to_explore.remove(next_cell)

        explored.append(next_cell)

        if (next_cell.col, next_cell.row) == maze.exit_point:

            path_found = retrace_steps(
                next_cell,
                maze.entry_point
            )
            break

        to_explore = find_valid_neighbors(
            cells,
            next_cell,
            to_explore,
            explored
        )

        cur_cell = next_cell

    if not path_found:

        print("Path not found!")
        return None

    maze.path = path_found

    path_to_return: str | None = compute_path(path_found, maze.entry_point)

    if not path_to_return:
        print("Something went wrong while computing the path")

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
