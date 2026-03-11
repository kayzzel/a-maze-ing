from enum import Enum


class WallsValues(str, Enum):

    NORTH = "13579BDF"
    SOUTH = "4567CDEF"
    EAST = "2367ABEF"
    WEST = "89ABCDEF"


def check_if_maze_closed(maze_input: list[str]) -> bool:

    if not all(hexa_val in WallsValues.NORTH for hexa_val in maze_input[0]):
        return False

    if not all(hexa_val in WallsValues.SOUTH for hexa_val in maze_input[-1]):
        return False

    if not all(hexa_val in WallsValues.WEST for hexa_val in [
        hexa_line[0] for hexa_line in maze_input
    ]):
        return False

    if not all(hexa_val in WallsValues.EAST for hexa_val in [
        hexa_line[-1] for hexa_line in maze_input
    ]):
        return False

    return True


def check_maze_input(maze_input: list[str]) -> bool:
    return all(
        (
            hexa in "0123456789ABCDEF"
            and len(maze_row) == len(maze_input[0])
        )
        for maze_row in maze_input
        for hexa in maze_row
    ) or check_if_maze_closed(maze_input)


"""

takes the hexadecimal value representing the walls
converts it into a tuple of boolean values

"""


def compute_walls(hexa: str) -> tuple[bool, bool, bool, bool]:

    bin_val: str = bin(int(hexa, 16))[2:]

    if not len(bin_val) == 4:

        bin_val = "0" * (4 - len(bin_val)) + bin_val

        # checks if the converted binary value is valid

        if not all(char in ["0", "1"] for char in bin_val):
            raise ValueError(
                f"Cannot compute walls with invalid value '{hexa}'!"
            )

    return (
        bin_val[0] == "1",
        bin_val[1] == "1",
        bin_val[2] == "1",
        bin_val[3] == "1"
    )


def is_in(
    x: int,
    y: int,
    start_pos: tuple[int, int],
    end_pos: tuple[int, int]
) -> bool:

    if (
        start_pos[0] <= x < end_pos[0]
    ) and (
        start_pos[1] <= y < end_pos[1]
    ):
        return True

    return False
