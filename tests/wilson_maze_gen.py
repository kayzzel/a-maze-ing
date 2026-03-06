from src.services.generation_algo.wilson import wilson
from src.utils.tui_display import print_maze


def main() -> None:
    size: tuple[int, int] = (
            11,  # height
            11   # width
            )

    maze = wilson(size, None)

    print("\n".join(line for line in maze))

    print()
    print_maze(maze)


if __name__ == "__main__":
    main()
