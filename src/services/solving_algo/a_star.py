from enum import Enum
from ...utils import compute_walls, check_maze_input
import random


class Walls(int, Enum):

    WEST = 0
    SOUTH = 1
    EAST = 2
    NORTH = 3


class PathCell:

    def __init__(
        self,
        hexa_val: str,
        coor: tuple[int, int],
        entry_coor: tuple[int, int],
        exit_coor: tuple[int, int]
    ) -> None:

        self.walls: tuple[
            bool, bool, bool, bool
        ] = compute_walls(hexa_val)

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
    maze_input: list[str],
    entry_coor: tuple[int, int],
    exit_coor: tuple[int, int]
) -> str | None:

    if not check_maze_input(maze_input):
        print("Invalid maze input!")
        return None

    cells: list[list[PathCell]] = []

    for row in range(len(maze_input)):

        cells.append([])

        for col in range(len(maze_input[0])):

            try:
                cells[row].append(PathCell(
                    maze_input[row][col],
                    (row, col),
                    entry_coor,
                    exit_coor
                ))
            except ValueError as ve:
                print(ve)
                return None

    current_cell: PathCell = cells[entry_coor[1]][entry_coor[0]]
    explored: list[PathCell] = [current_cell]
    to_explore: list[PathCell] = find_valid_neighbors(
        cells,
        current_cell,
        [],
        explored
    )
    path_found: list[PathCell] = []

    while (
        not path_found
        and len(explored) < len(maze_input) * len(maze_input[0])
    ):

        next_cell: PathCell | None = find_next_cell(to_explore)

        if not next_cell:
            break

        to_explore.remove(next_cell)

        explored.append(next_cell)

        if (next_cell.col, next_cell.row) == exit_coor:

            path_found = retrace_steps(
                next_cell,
                entry_coor
            )
            break

        to_explore = find_valid_neighbors(
            cells,
            next_cell,
            to_explore,
            explored
        )

        current_cell = next_cell

    if not path_found:

        print("Path not found!")
        return None

    path_to_return: str | None = compute_path(path_found, entry_coor)

    if not path_to_return:
        print("Something went wrong while computing the path")

    return path_to_return


def find_valid_neighbors(
    cells: list[list[PathCell]],
    cur_cell: PathCell,
    to_explore: list[PathCell],
    explored: list[PathCell]
) -> list[PathCell]:

    neighbors: list[PathCell] = []

    if not cur_cell.walls[Walls.NORTH]:
        neighbors.append(cells[cur_cell.row - 1][cur_cell.col])

    if not cur_cell.walls[Walls.SOUTH]:
        neighbors.append(cells[cur_cell.row + 1][cur_cell.col])

    if not cur_cell.walls[Walls.WEST]:
        neighbors.append(cells[cur_cell.row][cur_cell.col - 1])

    if not cur_cell.walls[Walls.EAST]:
        neighbors.append(cells[cur_cell.row][cur_cell.col + 1])

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
) -> list[PathCell]:

    cell: PathCell = destination

    path: list[PathCell] = []

    while (cell.col, cell.row) != entry_coor:

        path.append(cell)
        cell = cell.parent

    path.reverse()

    return path


def compute_path(
    path: list[PathCell],
    entry_coor: tuple[int, int]
) -> str | None:

    cur_row: int
    cur_col: int
    cur_col, cur_row = entry_coor

    directions: str = ""

    for cell in path:

        if cell.row == cur_row - 1:
            directions += "N"

        elif cell.row == cur_row + 1:
            directions += "S"

        elif cell.col == cur_col - 1:
            directions += "W"

        elif cell.col == cur_col + 1:
            directions += "E"

        else:
            return None

        cur_row, cur_col = cell.row, cell.col

    return directions
