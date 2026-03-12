def print_maze(maze: list[str]) -> None:

    height = len(maze)
    width = len(maze[0])

    # top border
    print("+---" * width + "+")

    for r in range(height):

        line_cells = "|"
        line_floor = "+"

        for c in range(width):

            value = int(maze[r][c], 16)

            east_closed = value & 2
            south_closed = value & 4

            # east wall
            if east_closed:
                line_cells += "   |"
            else:
                line_cells += "    "

            # south wall
            if south_closed:
                line_floor += "---+"
            else:
                line_floor += "   +"

        print(line_cells)
        print(line_floor)


def print_maze_with_path(
    maze: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
    path: str
) -> None:
    height = len(maze)
    width = len(maze[0])

    # Create a grid for path
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Start and end
    sy, sx = start
    ey, ex = end
    grid[sx][sy] = "S"
    grid[ex][ey] = "E"

    # Mark the path
    row, col = sx, sy
    for move in path:
        if move == "N":
            row -= 1
        elif move == "S":
            row += 1
        elif move == "W":
            col -= 1
        elif move == "E":
            col += 1
        # Only mark if not start or end
        if (col, row) != start and (col, row) != end:
            grid[row][col] = "*"

    # Print the maze with path
    print("+---" * width + "+")
    for r in range(height):
        line_cells = "|"
        line_floor = "+"
        for c in range(width):
            value = int(maze[r][c], 16)
            east_closed = value & 2
            south_closed = value & 4

            # Cell content
            cell_char = f" {grid[r][c]} "

            # East wall
            if east_closed:
                line_cells += cell_char + "|"
            else:
                line_cells += cell_char + " "

            # South wall
            if south_closed:
                line_floor += "---+"
            else:
                line_floor += "   +"
        print(line_cells)
        print(line_floor)
