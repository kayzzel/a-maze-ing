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

        self.distance: tuple[int, int] = self.calculate_distance(
            entry_coor,
            exit_coor
        )

        self.parent: "PathCell"

    def calculate_distance(
        self,
        entry_coor: tuple[int, int],
        exit_coor: tuple[int, int]
    ) -> tuple[int, int]:

        distance_from_entry: int = (
            abs(self.row - entry_coor[1])
            + abs(self.col - entry_coor[0])
        )
        distance_from_exit: int = (
            abs(self.row - exit_coor[1])
            + abs(self.col - exit_coor[0])
        )

        return (distance_from_entry, distance_from_exit)


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

    destination_found: bool = False

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
        not destination_found
        and len(explored) < len(maze_input) * len(maze_input[0])
    ):

        next_cell: PathCell | None = find_next_cell(to_explore)
        # print(f"\nNEXT CELL CHOSEN: {next_cell.col, next_cell.row} DISTANCE: {next_cell.distance}\n\n")
        if not next_cell:
            break
        to_explore.remove(next_cell)
        explored.append(next_cell)
        # if is_neighbor(current_cell, next_cell, cells):
        # next_cell.parent = current_cell
        if (next_cell.col, next_cell.row) == exit_coor:
            print("Found the exit!")
            path_found = retrace_steps(
                next_cell,
                entry_coor
            )
            destination_found = True
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


"""
def is_neighbor(
    cell: PathCell,
    neighbor: PathCell,
    cells: list[list[PathCell]]
) -> bool:

    neighbors: list[PathCell] = []

    if not cell.walls[Walls.NORTH]:
        neighbors.append(cells[cell.row - 1][cell.col])

    if not cell.walls[Walls.SOUTH]:
        neighbors.append(cells[cell.row + 1][cell.col])

    if not cell.walls[Walls.WEST]:
        neighbors.append(cells[cell.row][cell.col - 1])

    if not cell.walls[Walls.EAST]:
        neighbors.append(cells[cell.row][cell.col + 1])

    return neighbor in neighbors
"""


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

        if not (neighbor in to_explore or neighbor in explored):
            to_explore.append(neighbor)
            neighbor.parent = cur_cell

    return to_explore


def find_next_cell(to_explore: list[PathCell]) -> PathCell | None:

    if not to_explore:
        return None
    sorted_list: list[PathCell] = sorted(
        to_explore,
        key=lambda cell: cell.distance[0] + cell.distance[1]
    )
    if any(
        (cell.distance[0] + cell.distance[1]) ==
        (sorted_list[0].distance[0] + sorted_list[0].distance[1])
        for cell in sorted_list[1:]
    ):
        sorted_list = [
            cell
            for cell in to_explore
            if (cell.distance[0] + cell.distance[1]) ==
            (sorted_list[0].distance[0] + sorted_list[0].distance[1])
        ]
        sorted_list = sorted(
            sorted_list,
            key=lambda cell: cell.distance[1]
        )
        # print("same overall distance, sorting by distance from exit")
        # for cell in sorted_list:
        #    print(f"cell in sorted list: {cell.row, cell.col} distance: {cell.distance}")
        # print("\n\n")
        if any(
            cell.distance[1] == sorted_list[0].distance[1]
            for cell in sorted_list[1:]
        ):
            sorted_list = [
                cell
                for cell in to_explore
                if cell.distance[1] == sorted_list[0].distance[1]
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
