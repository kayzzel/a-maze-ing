# need to move algorithms in the same directory
from typing import Callable


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

        self.pattern_cells: set[tuple[int, int]] = set()

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


class MazeGenerator:

    def __init__(
        self,
        maze_sz: tuple[int, int],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        is_perfect: bool,
        seed: int | None
    ) -> None:

        from ..services.generation_algo.rec_backtrack import rec_backtrack
        from ..services.solving_algo.a_star import a_star

        self.set_maze_sz(maze_sz)
        self.set_entry_exit_point(entry_point, "entry")
        self.set_entry_exit_point(exit_point, "exit")
        self.set_perfect(is_perfect)
        self.set_seed(seed)

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

        for val in sz:

            if not isinstance(val, int) or val <= 0:
                raise ValueError("invalid size for the maze")

        self.__maze_sz: tuple[int, int] = sz
        print(f"successfully modified maze size to {sz}")

    def get_maze_sz(self) -> tuple[int, int]:

        return self.__maze_sz

    def set_entry_exit_point(
        self,
        point: tuple[int, int],
        point_type: str
    ) -> None:

        for val in point:

            if not isinstance(val, int):
                raise ValueError(
                    f"invalid {point_type} coordinates for the maze"
                )

        if not (
            0 <= point[0] < self.__maze_sz[0]
            and 0 <= point[1] < self.__maze_sz[1]
        ):
            raise ValueError(
                f"invalid {point_type} coordinates for the maze\n"
                "coordinates are outside of the maze's bounds"
            )

        if point_type == "entry":
            self.__entry_point: tuple[int, int] = point

        elif point_type == "exit":
            self.__exit_point: tuple[int, int] = point

        print(f"successfully changed {point_type} coordinates to {point}")

    def get_entry_exit_point(self) -> tuple[
        tuple[int, int],
        tuple[int, int]
    ]:
        return (self.__entry_point, self.__exit_point)

    def set_perfect(self, perfection: bool) -> None:

        if not isinstance(perfection, bool):
            raise ValueError("invalid value for the perfection parameter")

        self.__is_perfect: bool = perfection
        print(f"successfully changed the maze's perfection to {perfection}")

    def get_perfect(self) -> bool:

        return self.__is_perfect

    def set_seed(self, seed: int | None) -> None:

        if not isinstance(seed, int) and seed is not None:
            raise ValueError("invalid value for the seed")

        if isinstance(seed, int) and seed < 0:
            raise ValueError("invalid value for the seed")

        self.__seed: int | None = seed
        print(f"sucessfully changed the seed to {seed}")

    def get_seed(self) -> int | None:

        return self.__seed

    def initialize_maze(self) -> Maze:

        return Maze(self.__maze_sz, self.__entry_point, self.__exit_point)

    def generate_maze(self) -> Maze:

        from ..utils.generation_utils import maze_to_imperfect

        maze: Maze = self.gen_algo(
            self.__maze_sz,
            self.__entry_point,
            self.__exit_point,
            self.__seed
        )

        if not self.__is_perfect:
            maze_to_imperfect(maze, self.__seed)

        return maze

    def write_to_output(self, maze: Maze, output_filename: str) -> None:

        try:

            with open(output_filename) as output:

                output.write("\n".join(maze.maze_to_hexa()))
                output.write("\n")
                output.write(str(maze.entry_point) + "\n")
                output.write(str(maze.exit_point) + "\n")
                output.write(maze.path_dirs + "\n")

        except OSError as err:

            print(err)

        return None

    def calculate_path(self, maze: Maze) -> str | None:

        return self.solve_algo(maze)
