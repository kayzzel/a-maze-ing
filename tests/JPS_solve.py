from src.utils.tui_display import print_maze, print_maze_with_path
from src.services.generation_algo import wilson
from src.services.solving_algo import jump_point_search


def main() -> None:
    size: tuple[int, int] = (
            27,  # height
            27   # width
            )

    start: tuple[int, int] = (
            0,
            0
            )

    end: tuple[int, int] = (
            10,
            11
            )

    maze = wilson(size, start, end)
    path = jump_point_search(maze, start, end)

    print("\n".join(line for line in maze))

    print()
    print_maze(maze)

    print()
    print(path)

    print()
    if isinstance(path, str):
        print_maze_with_path(maze, start, end, path)


if __name__ == "__main__":
    main()
