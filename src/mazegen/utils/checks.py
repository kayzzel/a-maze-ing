from enum import Enum


class WallsValues(str, Enum):
    """
        Description:
    An enumeration of hexadecimal character sets used to identify which
    cells have a closed wall on a given side. Each member holds a string
    of hex characters where the corresponding wall bit is set

        Attributes:
    NORTH -> hex characters where the north wall bit is set
    SOUTH -> hex characters where the south wall bit is set
    EAST -> hex characters where the east wall bit is set
    WEST -> hex characters where the west wall bit is set
    """

    NORTH = "13579BDF"
    SOUTH = "4567CDEF"
    EAST = "2367ABEF"
    WEST = "89ABCDEF"


def check_if_maze_closed(maze_input: list[str]) -> bool:
    """
        Description:
    Verify that the maze is fully enclosed by checking that every cell
    on each border row or column has a wall on the side facing outward

        Parameters:
    maze_input -> the maze as a list of hexadecimal row strings

        Returns value:
    return True if all four borders are closed, False otherwise
    """

    # Every cell on the top row must have a north wall
    if not all(hexa_val in WallsValues.NORTH for hexa_val in maze_input[0]):
        return False

    # Every cell on the bottom row must have a south wall
    if not all(hexa_val in WallsValues.SOUTH for hexa_val in maze_input[-1]):
        return False

    # Every cell on the left column must have a west wall
    if not all(hexa_val in WallsValues.WEST for hexa_val in [
        hexa_line[0] for hexa_line in maze_input
    ]):
        return False

    # Every cell on the right column must have an east wall
    if not all(hexa_val in WallsValues.EAST for hexa_val in [
        hexa_line[-1] for hexa_line in maze_input
    ]):
        return False

    return True


def check_maze_input(maze_input: list[str]) -> bool:
    """
        Description:
    Validate that the maze input contains only valid hexadecimal characters
    and that every row has the same length, then confirm the maze is
    fully enclosed by calling check_if_maze_closed

        Parameters:
    maze_input -> the maze as a list of hexadecimal row strings

        Returns value:
    return True if the input is well-formed and the maze is closed,
    False otherwise
    """

    return all(
        (
            hexa in "0123456789ABCDEF"
            and len(maze_row) == len(maze_input[0])
        )
        for maze_row in maze_input
        for hexa in maze_row
    ) or check_if_maze_closed(maze_input)


def compute_walls(hexa: str) -> tuple[bool, bool, bool, bool]:
    """
        Description:
    Convert a single hexadecimal character representing a cell's wall
    state into a tuple of four booleans, one per wall direction

        Parameters:
    hexa -> a single hexadecimal character encoding the cell's walls

        Returns value:
    return a tuple of (W, S, E, N) booleans where True means the
    wall is present, or raise a ValueError if the value is invalid
    """

    # Convert the hex character to a 4-bit binary string
    bin_val: str = bin(int(hexa, 16))[2:]

    # Pad to 4 bits if the value is less than 4 digits
    if not len(bin_val) == 4:
        bin_val = "0" * (4 - len(bin_val)) + bin_val

        # Ensure the padded binary string contains only valid characters
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
    """
        Description:
    Check whether a point is inside a rectangular region defined by
    two corner positions

        Parameters:
    x -> the x coordinate of the point to check
    y -> the y coordinate of the point to check
    start_pos -> the (x, y) top-left corner of the region (inclusive)
    end_pos -> the (x, y) bottom-right corner of the region (exclusive)

        Returns value:
    return True if the point lies within the region, False otherwise
    """

    if (
        start_pos[0] <= x < end_pos[0]
    ) and (
        start_pos[1] <= y < end_pos[1]
    ):
        return True

    return False
