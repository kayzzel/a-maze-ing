from random import Random, randint


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

# defines all the directions
DIRECTIONS: list[CellCoords] = [
        (-1, 0),  # North
        (1, 0),   # South
        (0, -1),  # East
        (0, 1),   # West
        ]


def neighbors(
        cell: CellCoords,
        size: tuple[int, int],
        pattern_cells: set[CellCoords]
        ) -> list[CellCoords]:
    """
    get a cell and return the list of all it's available neighbors
    """

    # unpack the size tuple in height and width
    width: int = size[0]
    height: int = size[1]
    row, col = cell

    neighbors_list: list[CellCoords] = []
    # DIRECTIONS likely contains directions such as:
    # [(1,0), (-1,0), (0,1), (0,-1)]
    for dir_row, dir_col in DIRECTIONS:

        # Compute neighbor coordinates
        new_row, new_col = row + dir_row, col + dir_col
        neighbor: CellCoords = (new_row, new_col)

        # Check the neighbor is inside the grid
        if (0 <= new_row < height and 0 <= new_col < width
                and neighbor not in pattern_cells):

            # Yield the neighbor cell
            neighbors_list.append(neighbor)

    return neighbors_list


def walk(
        cell: CellCoords,
        visited: dict[CellCoords, int],
        unvisited: set[CellCoords],
        path: list[CellCoords],
        size: tuple[int, int],
        pattern_cells: set[CellCoords],
        rnd: Random
        ) -> list[CellCoords]:
    """
    Perform a random walk until we reach a visited maze cell
    """
    while cell in unvisited:

        # Choose a random neighboring cell
        # uses the seeded random for the choice
        cell = rnd.choice(neighbors(cell, size, pattern_cells))

        # If we revisit a cell in our current path
        # we found a loop
        if cell in visited:

            # Index where the loop started
            loop: int = visited[cell]

            # Remove the loop by truncating the path
            path = path[:loop+1]

            # Rebuild the visited dictionary
            visited = {p: i for i, p in enumerate(path)}

        else:
            # Otherwise extend the path
            path.append(cell)

            # Record the position of this cell in the path
            visited[cell] = len(path)-1

    return path


def carve_path(
            maze: Maze,
            path: list[CellCoords],
            unvisited: set[CellCoords],
            unvisited_list: list[CellCoords]
        ) -> None:

    for index in range(len(path) - 1):

        row, col = path[index]
        next_cell = path[index + 1]

        # Create a bidirectional connection between the two cells
        if next_cell == (row - 1, col):
            maze.cells[row][col].walls["N"] = False
            maze.cells[row - 1][col].walls["S"] = False
        elif next_cell == (row + 1, col):
            maze.cells[row][col].walls["S"] = False
            maze.cells[row + 1][col].walls["N"] = False
        elif next_cell == (row, col - 1):
            maze.cells[row][col].walls["W"] = False
            maze.cells[row][col - 1].walls["E"] = False
        elif next_cell == (row, col + 1):
            maze.cells[row][col].walls["E"] = False
            maze.cells[row][col + 1].walls["W"] = False

        step_cell: Cell = Cell(col, row)
        step_cell.walls = maze.cells[row][col].walls
        maze.gen_steps.append(step_cell)

        next_step_cell: Cell = Cell(*next_cell[::-1])
        next_step_cell.walls = maze.cells[next_cell[0]][next_cell[1]].walls
        maze.gen_steps.append(next_step_cell)

        # Mark the current cell as visited in the maze
        if (row, col) in unvisited:
            unvisited.remove((row, col))
            unvisited_list.remove((row, col))


def wilson(
        size: tuple[int, int],
        entry_point: CellCoords,
        exit_point: CellCoords,
        seed: int | None
        ) -> Maze:
    """
    get a size (height, width) and create a maze by using the wilson algorith
    """

    # Create a rnd: Random wich is the base form the choices so that:
    rnd: Random

    # Whene no seed is given it generate one randomly
    if seed is None:
        rnd = Random(randint(0, 1000000000))

    # Whene there is a seed given it put the base Random to the seed
    # to be able to generate the same maze with the same seed
    elif isinstance(seed, int) and seed >= 0:
        rnd = Random(seed)

    # When the seed format is wrong it raises a ValueError
    else:
        raise ValueError("seed must be a positive integer")

    maze: Maze = Maze(size, entry_point, exit_point)

    # unpack the size tuple in height and width
    width: int = size[0]
    height: int = size[1]

    pattern_cells: set[CellCoords] = create_pattern(size)

    # All cells start as unvisited
    unvisited: set[CellCoords] = {
        (row, col)
        for row in range(height)
        for col in range(width)
        if (row, col) not in pattern_cells
    }
    unvisited_list: list[CellCoords] = list(unvisited)

    # Pick a random starting cell and mark it visited
    # This becomes the initial tree of the maze
    # uses the seeded random for the choice
    first: CellCoords = rnd.choice(list(unvisited))
    unvisited.remove(first)
    unvisited_list.remove(first)

    # Continue until every cell is added to the maze
    while unvisited:

        # Pick a random unvisited cell to start a random walk
        # uses the seeded random for the choice
        cell: CellCoords = rnd.choice(unvisited_list)

        # Path of the current random walk
        path: list[CellCoords] = [cell]

        # Track visited cells in the current walk
        # value = index of that cell in the path
        visited: dict[CellCoords, int] = {cell: 0}

        # Perform a random walk until we reach a visited maze cell
        path = walk(cell, visited, unvisited, path, size, pattern_cells, rnd)

        # Carve the path into the maze
        carve_path(maze, path, unvisited, unvisited_list)

    # Return the completed maze graph
    return maze


def create_pattern(size: tuple[int, int]) -> set[CellCoords]:
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

    return set(pattern_cells)
