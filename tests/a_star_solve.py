from src.services import a_star


def test_solving() -> None:

    input_filename: str = "tests/input_maze.txt"
    path_name: str = "tests/path.txt"

    with open(input_filename) as file:
        maze_input: list[str] = [line.rstrip() for line in file]

    with open(path_name) as path_file:
        lines: list[str] = path_file.readlines()
        entry: list[str] = lines[0].rstrip().split(",")
        entry_coor: tuple[int, int] = (int(entry[0]), int(entry[1]))
        exiting: list[str] = lines[1].rstrip().split(",")
        exit_coor: tuple[int, int] = (int(exiting[0]), int(exiting[1]))
        path: str = lines[2].rstrip()

    """
    maze_input: list[str] = [
        "D3D53",
        "945DA",
        "A9156",
        "E82D3",
        "D6C7E"
    ]

    entry_coor: tuple[int, int] = (1, 3)
    exit_coor: tuple[int, int] = (3, 0)

    path1: str = "NEEENNW"
    path2: str = "ENEENNW"
    """

    a_star_path: str | None = a_star(maze_input, entry_coor, exit_coor)

    if not a_star_path or a_star_path != path:
        print(f"Solving failed: path found by algorithm is {a_star_path} instead of {path}\n")
    else:
        print("Solving succeeded! :)")


if __name__ == "__main__":

    test_solving()
