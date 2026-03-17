# need to move algorithms in the same directory
from typing import Callable
from .display import print_maze, print_maze_with_path
from .utils import check_maze_input


class Cell:
    """
        Description:
    Represents a single cell in the maze grid, storing its position,
    wall states, and whether it has been visited during generation

        Parameters:
    x -> the column index of the cell
    y -> the row index of the cell

        Attributes:
    row -> the row index of the cell
    col -> the column index of the cell
    coor -> the (col, row) coordinates of the cell
    walls -> a dict mapping direction keys (N, S, E, W) to booleans,
             True if the wall is present, False if it has been carved
    visited -> True if the cell has been visited during maze generation
    """

    def __init__(
        self,
        x: int,
        y: int
    ) -> None:

        self.row: int = y
        self.col: int = x
        self.coor: tuple[int, int] = (x, y)

        # All walls start closed; they are carved open during generation
        self.walls: dict[str, bool] = {
            "N": True,
            "S": True,
            "W": True,
            "E": True
        }

        self.visited: bool = False


class Maze:
    """
        Description:
    Represents a complete maze grid along with its entry and exit points,
    generation and solving step histories, and the computed solution path

        Parameters:
    size -> the size of the maze as (width, height)
    entry_point -> the (col, row) coordinate of the maze entry
    exit_point -> the (col, row) coordinate of the maze exit

        Attributes:
    sz -> the maze size as (width, height)
    width -> the number of columns
    height -> the number of rows
    entry_point -> the entry coordinate
    exit_point -> the exit coordinate
    cells -> the 2D grid of Cell instances
    gen_steps -> the ordered list of Cells visited during generation,
                 used to animate the generation process
    solving_steps -> the ordered list of Cells visited during solving,
                     used to animate the solving process
    path -> the solution path as an ordered list of (col, row) coordinates
    path_dirs -> the solution path as a string of direction letters (NSEW)
    pattern_cells -> the set of (row, col) coordinates reserved as
                     pattern cells that cannot be carved into
    """

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

        # Build the full grid of Cells
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

        self.pattern_cells: set[tuple[int, int]] = set()

    def maze_to_hexa(self) -> list[str]:
        """
            Description:
        Convert the maze grid into a list of hexadecimal strings, one per
        row. Each character encodes the wall state of a single cell as a
        4-bit value where each bit represents one wall (N=1, E=2, S=4, W=8)

            Returns value:
        return a list of strings where each string is the hexadecimal
        encoding of one row of the maze
        """

        # Each wall direction maps to a bit in the cell's hex value
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

                # Accumulate the bit value for each present wall
                for wall, state in cell.walls.items():

                    if state:
                        val |= walls_values[wall]

                # Map the 4-bit value to its hexadecimal character
                hexa_maze[row] += ("0123456789ABCDEF")[val]

        return hexa_maze


class MazeGenerator:
    """
        Description:
    Manages maze configuration, generation, and solving. Stores all
    generation parameters behind private setters that validate their
    input, and exposes methods to generate, solve, and write mazes

        Parameters:
    maze_sz -> the size of the maze as (width, height)
    entry_point -> the (col, row) coordinate of the maze entry
    exit_point -> the (col, row) coordinate of the maze exit
    is_perfect -> True if the maze should have no loops
    seed -> an optional positive integer to seed the random generator

        Attributes:
    gen_algo -> the generation algorithm callable, defaults to rec_backtrack
    solve_algo -> the solving algorithm callable, defaults to a_star
    """

    def __init__(
        self,
        maze_sz: tuple[int, int],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        is_perfect: bool = True,
        seed: int | None = None
    ) -> None:
        from .algorithms.rec_backtrack import rec_backtrack
        from .algorithms.a_star import a_star

        for val in maze_sz:

            if not isinstance(val, int) or not (5 <= val <= 201):
                raise ValueError("Invalid size {sz} for the maze")

        self.__maze_sz: tuple[int, int] = maze_sz
        self.__entry_point: tuple[int, int] = (-1, -1)
        self.set_entry_exit_point(exit_point, "exit")
        self.set_entry_exit_point(entry_point, "entry")
        self.set_perfect(is_perfect)
        self.set_seed(seed)

        # Default to recursive backtracking for generation and A* for solving
        self.gen_algo: Callable[
                    [
                        tuple[int, int],
                        tuple[int, int],
                        tuple[int, int],
                        int | None
                    ], Maze
                ] = rec_backtrack

        self.solve_algo: Callable[[Maze], str | None] = a_star

    def set_maze_sz(self, sz: tuple[int, int]) -> None:
        """
            Description:
        Validate and store the maze size. Both dimensions must be positive
        integers

            Parameters:
        sz -> the new maze size as (width, height)
        """

        for val in sz:

            if not isinstance(val, int) or not (5 <= val <= 201):
                raise ValueError("Invalid size {sz} for the maze")

        for point in [self.__entry_point, self.__exit_point]:

            if sz[0] <= point[0] or sz[1] <= point[1]:
                raise ValueError(
                    f"Maze size {sz} is too small "
                    "for the entry/exit coordinates"
                )

        self.__maze_sz = sz

    def get_maze_sz(self) -> tuple[int, int]:
        """
            Description:
        Return the current maze size

            Returns value:
        return the maze size as (width, height)
        """

        return self.__maze_sz

    def set_entry_exit_point(
        self,
        point: tuple[int, int],
        point_type: str
    ) -> None:
        """
            Description:
        Validate and store an entry or exit coordinate. Both values must
        be positive integers and the point must lie within the maze bounds

            Parameters:
        point -> the (col, row) coordinate to set
        point_type -> either "entry" or "exit" to indicate which point
                      is being set
        """

        # Ensure both coordinate values are positive integers
        for val in point:

            if not isinstance(val, int):
                raise ValueError(
                    f"Invalid {point_type} coordinates for the maze"
                )

        # Ensure the point lies within the current maze boundaries
        if not (
            0 <= point[0] < self.__maze_sz[0]
            and 0 <= point[1] < self.__maze_sz[1]
        ):
            raise ValueError(
                f"Invalid {point_type} coordinates for the maze\n"
                "Coordinates are outside of the maze's bounds"
            )

        if point_type == "entry":
            if point == self.__exit_point:
                raise ValueError(
                    f"Invalid {point_type} coordinates for the maze\n"
                    "Entry coordinates are the same as the exit coordinates"
                )
            self.__entry_point = point

        elif point_type == "exit":
            if point == self.__entry_point:
                raise ValueError(
                    f"Invalid {point_type} coordinates for the maze\n"
                    "Exit coordinates are the same as the entry coordinates"
                )
            self.__exit_point: tuple[int, int] = point

    def get_entry_exit_point(self) -> tuple[
        tuple[int, int],
        tuple[int, int]
    ]:
        """
            Description:
        return the entry and exit point that are private attribute in the maze

            Returns value:
        entry_point -> (x, y) coordinate in cells
        exit_point-> (x, y) coordinate in cells
        """
        return (self.__entry_point, self.__exit_point)

    def set_perfect(self, perfection: bool) -> None:
        """
            Description:
        Validate and store the perfect maze flag

            Parameters:
        perfection -> True if the maze should have no loops, False otherwise
        """

        if not isinstance(perfection, bool):
            raise ValueError(
                f"Invalid value {perfection} "
                "for the perfection parameter"
            )

        self.__is_perfect: bool = perfection

    def get_perfect(self) -> bool:
        """
            Description:
        Return the current perfect maze flag

            Returns value:
        return True if the maze is set to be perfect, False otherwise
        """

        return self.__is_perfect

    def set_seed(self, seed: int | None) -> None:
        """
            Description:
        Validate and store the random seed. The seed must be a non-negative
        integer or None

            Parameters:
        seed -> a non-negative integer to seed the random generator,
                or None to use a random seed
        """

        if not isinstance(seed, int) and seed is not None:
            raise ValueError(f"Invalid value {seed} for the seed")

        if isinstance(seed, int) and seed < 0:
            raise ValueError(f"Invalid value {seed} for the seed")

        self.__seed: int | None = seed

    def get_seed(self) -> int | None:
        """
            Description:
        returns the seed that is set for the maze_generator

            Returns value:
        the seed, a positive integer
        """

        return self.__seed

    def set_gen_algo(self, algorithm: Callable) -> None:
        """
            Description:
        set an algorithm in only the right function an in the list of
        authorised algorithm

            Parameters:
        the function that represent the algorithme
        """

        from .algorithms.rec_backtrack import rec_backtrack
        from .algorithms.wilson import wilson

        if not callable(algorithm) or algorithm not in [
            wilson,
            rec_backtrack
        ]:
            raise ValueError(
                "Invalid generation algorithm provided\n"
                "Choose between 'wilson' and 'rec_backtrack'"
            )

        self.gen_algo = algorithm

    def set_solve_algo(self, algorithm: Callable) -> None:
        """
            Description:
        set an algorithm in only the right function an in the list of
        authorised algorithm

            Parameters:
        the function that represent the algorithme
        """

        from .algorithms.a_star import a_star
        from .algorithms.jump_point_search import jump_point_search

        if not callable(algorithm) or algorithm not in [
            a_star,
            jump_point_search
        ]:
            raise ValueError(
                "Invalid generation algorithm provided\n"
                "Choose between 'a_star' and 'jump_point_search'"
            )

        self.solve_algo = algorithm

    def initialize_maze(self) -> Maze:
        """
            Description:
        Create and return a blank Maze with no walls carved, using the
        current size, entry, and exit configuration

            Returns value:
        return a new empty Maze instance
        """

        return Maze(self.__maze_sz, self.__entry_point, self.__exit_point)

    def generate_maze(self) -> Maze:
        """
            Description:
        Generate a maze using the current generation algorithm and
        configuration. If the maze is not set to be perfect, additional
        walls are removed to introduce loops

            Returns value:
        return the fully generated Maze instance
        """

        from .utils import maze_to_imperfect

        maze: Maze = self.gen_algo(
            self.__maze_sz,
            self.__entry_point,
            self.__exit_point,
            self.__seed
        )

        # Remove extra walls to create loops if a perfect maze is not required
        if not self.__is_perfect:
            maze_to_imperfect(maze, self.__seed)

        return maze

    def write_to_output(self, maze: Maze, output_filename: str) -> bool:
        """
            Description:
        Write the maze's hexadecimal grid, entry and exit coordinates,
        and solution path directions to a text file

            Parameters:
        maze -> the Maze instance to serialize
        output_filename -> the path to the output file to write to
        """

        try:

            with open(output_filename, "w") as output:

                # Write each row of the hex grid on its own line
                output.write("\n".join(maze.maze_to_hexa()))
                output.write("\n\n")
                output.write(str(maze.entry_point) + "\n")
                output.write(str(maze.exit_point) + "\n")
                self.solve_maze(maze)
                output.write(maze.path_dirs + "\n")

        except OSError as err:

            print(err)
            return False

        return True

    def solve_maze(self, maze: Maze) -> str | None:
        """
            Description:
        Solve the given maze using the current solving algorithm

            Parameters:
        maze -> the Maze instance to solve

            Returns value:
        return the solution path as a string of direction letters (NSEW),
        or None if no path exists
        """

        return self.solve_algo(maze)

    def tui_display_maze(
        self,
        hexa_maze: list[str],
        path: str | None = None,
        entry_point: tuple[int, int] | None = None,
        exit_point: tuple[int, int] | None = None
    ) -> None:
        """
            Description:
        display a given maze in the terminal,
        and if a path is provided then also print it with the start and exit

            Parameters:
        hexa_maze -> A maze in hexadecimal values in which each bit represent
                     a wall (W, S, E, N)
        path -> The direction to go from the start to the exit (N, S, E, W)
        entry_point -> the coordinate of the start (x, y)
        exit_point -> the coordinate of the end (x, y)
        """

        if not hexa_maze:
            print("Error: No maze provided")
            return None

        if not check_maze_input(hexa_maze):
            print("Error: Invalid maze input")
            return None

        if not path or not entry_point or not exit_point:
            print_maze(hexa_maze)
            return None

        if entry_point == exit_point:
            print("Error: Entry and exit point are the same")
            return None

        print_maze_with_path(
            hexa_maze,
            path,
            entry_point,
            exit_point
        )
