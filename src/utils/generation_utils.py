from random import Random, randint


# define the type of a cell
CellCoords = tuple[int, int]


def create_pattern(
        size: tuple[int, int],
        start: CellCoords,
        end: CellCoords
        ) -> set[CellCoords]:
    """
    take the size (height, width) of the maze and create
    the 42 patern centered
    """

    # unpack the size tuple in height and width
    width, height = size

    # create the pattern only if the maze is big enougth (10*10)
    if height < 10 or width < 10:
        return set()

    # get the padding of the pattern to center it
    start_row: int = height // 2 - 2
    start_col: int = width // 2 - 3

    # create the patern to the up left corner
    pattern_cells: list[CellCoords] = [
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2),    # 4
        (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4),    # 2
        (3, 4), (4, 4), (4, 5), (4, 6)
    ]

    # add the padding to the patern
    for index in range(len(pattern_cells)):

        new_cell: CellCoords = (
                pattern_cells[index][0] + start_row,
                pattern_cells[index][1] + start_col
                )

        pattern_cells[index] = new_cell

    # If the start or the end is in the patern it return an empty set
    if start[::-1] in pattern_cells or end[::-1] in pattern_cells:
        return set()

    #  return the patern so that it could be integrated in the maze
    return set(pattern_cells)


def maze_to_imperfect(maze: Maze) -> None:
    pass
