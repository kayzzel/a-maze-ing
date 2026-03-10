# need to move algorithms in the same directory
from .algorithms import rec_backtrack, jump_point_search


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

        self.size: tuple[int, int] = size

        self.entry_point: tuple[int, int] = entry_point
        self.exit_point: tuple[int, int] = exit_point

        self.cells: list[list[Cell]] = [
            [
                Cell(col, row)
                for col in range(self.maze_sz[0])
            ]
            for row in range(self.maze_sz[1])
        ]

        self.gen_steps: list[Cell] = []
        self.solving_steps: list[Cell] = []


class MazeGenerator:

    def __init__(self) -> None:

        self.gen_algo: callable = rec_backtrack
        self.solve_algo: callable = jump_point_search

    def generate_maze(
        self,
        maze_sz: tuple[int, int],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        is_perfect: bool,
        seed: int | None
    ) -> Maze:

        return self.gen_algo(maze_sz, entry_point, exit_point, seed)

    def write_to_output(self.maze: Maze, output_filename: str) -> None:

        hexa_maze: list[str] = maze_to_hexa(maze)
        path: list[str] = self.calculate_path(maze)

        try:

            with open(output_filename) as output:

                output.write("\n".join(hexa_maze))
                output.write("\n")
                output.write(str(maze.entry_point) + "\n")
                output.write(str(maze.exit_point) + "\n")
                output.write(path + "\n")

        except OSError as err:

            print(err)

        return None

    def calculate_path(self, maze: Maze) -> str:

        return self.solve_algo(maze)

    @staticmethod
    def maze_to_hexa(maze: Maze) -> list[str]:

        walls_values: dict[str, int] = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8
        }

        hexa_maze: list[str] = []

        for row in maze:

            for cell in row:

                val: int = 0

                for wall, state in cell.walls.items():
                    if state:
                        val |= walls_values[wall]

                hexa_maze[row] += hex(val)[2:]

        return maze_to_hexa
