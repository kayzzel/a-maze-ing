from src.services.generation_algo.wilson import wilson
from src.utils.tui_display import print_maze


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

    print("\n".join(line for line in maze))

    print()
    print_maze(maze)


if __name__ == "__main__":
    main()
