from random import Random, randint
# from src.models.maze_generator import Maze, Cell


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


def maze_to_imperfect(
        maze: Maze,
        seed: int | None
        ) -> None:

    pattern: set[CellCoords] = create_pattern(
            maze.sz, maze.entry_point, maze.exit_point
        )

    rnd: Random
    if not seed:
        rnd = Random(randint(0, 1000000000))

    elif isinstance(seed, int) and seed > 0:
        rnd = Random(seed)

    else:
        raise ValueError("Wrong seed format")

    for row in range(maze.height):
        for col in range(maze.width):

            cell: Cell = maze.cells[row][col]

            if len([True for wall in cell.walls.values() if wall]) != 3:
                continue

            if (cell.walls["N"] and cell.walls["W"] and cell.walls["E"] and
                    row - 1 >= 0 and (row - 1, col) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["N"] = False
                maze.gen_steps.append(cell)

                maze.cells[row - 1][col].walls["S"] = False
                maze.gen_steps.append(maze.cells[row - 1][col])

            elif (cell.walls["S"] and cell.walls["W"] and cell.walls["E"] and
                    row + 1 < maze.height and (row + 1, col) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["S"] = False
                maze.gen_steps.append(cell)

                maze.cells[row + 1][col].walls["N"] = False
                maze.gen_steps.append(maze.cells[row + 1][col])

            elif (cell.walls["E"] and cell.walls["S"] and cell.walls["N"] and
                    col + 1 < maze.width and (row, col + 1) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["E"] = False
                maze.gen_steps.append(cell)

                maze.cells[row][col + 1].walls["W"] = False
                maze.gen_steps.append(maze.cells[row][col + 1])

            elif (cell.walls["W"] and cell.walls["S"] and cell.walls["N"] and
                    col - 1 >= 0 and (row, col - 1) not in pattern and
                    rnd.randint(0, 3) == 0):
                cell.walls["W"] = False
                maze.gen_steps.append(cell)

                maze.cells[row][col - 1].walls["E"] = False
                maze.gen_steps.append(maze.cells[row][col - 1])
