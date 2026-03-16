def print_maze(maze: list[str]) -> None:
    """
        Description:
    Render a maze to stdout as a grid of ASCII characters using the
    hexadecimal wall encoding of each cell. East and south walls are
    derived from the cell's hex value using bit masking

        Parameters:
    maze -> the maze as a list of hexadecimal row strings
    """

    height = len(maze)
    width = len(maze[0])

    # Top border spanning the full width of the maze
    print("\033[94m" + "+---" * width + "+" + "\033[0m")

    for r in range(height):

        line_cells = "\033[94m" + "|" + "\033[0m"
        line_floor = "\033[94m" + "+" + "\033[0m"

        for c in range(width):

            value = int(maze[r][c], 16)

            # Extract the east and south wall bits from the hex value
            east_closed = value & 2
            south_closed = value & 4

            # East wall
            if east_closed:
                line_cells += "\033[94m" + "   |" + "\033[0m"
            else:
                line_cells += "\033[94m" + "    " + "\033[0m"

            # South wall
            if south_closed:
                line_floor += "\033[94m" + "---+" + "\033[0m"
            else:
                line_floor += "\033[94m" + "   +" + "\033[0m"

        print(line_cells)
        print(line_floor)


def print_maze_with_path(
    maze: list[str],
    path: str,
    start: tuple[int, int],
    end: tuple[int, int]
) -> None:
    """
        Description:
    Render a maze to stdout with the solution path overlaid. The start
    cell is marked S, the end cell is marked E, and each step along the
    path is marked with an asterisk. Walls are drawn the same way as in
    print_maze using bit masking on the hex cell values

        Parameters:
    maze -> the maze as a list of hexadecimal row strings
    start -> the (col, row) coordinate of the entry point
    end -> the (col, row) coordinate of the exit point
    path -> the solution path as a string of direction letters (NSEW)
    """

    height = len(maze)
    width = len(maze[0])

    # Initialize the character grid with empty cells
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Mark the start and end cells
    sy, sx = start
    ey, ex = end
    grid[sx][sy] = "\033[96m" + "S" + "\033[0m"
    grid[ex][ey] = "\033[96m" + "E" + "\033[0m"

    # Walk the path and mark each intermediate cell with an asterisk
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

        # Leave the start and end markers unchanged
        if (col, row) != start and (col, row) != end:
            grid[row][col] = "\033[93m" + "*" + "\033[0m"

    # Print the maze with the path overlay
    print("\033[94m" + "+---" * width + "+" + "\033[0m")

    for r in range(height):

        line_cells = "\033[94m" + "|" + "\033[0m"
        line_floor = "\033[94m" + "+" + "\033[0m"

        for c in range(width):

            value = int(maze[r][c], 16)

            # Extract the east and south wall bits from the hex value
            east_closed = value & 2
            south_closed = value & 4

            cell_char = f" {grid[r][c]} "

            # East wall
            if east_closed:
                line_cells += cell_char + "\033[94m" + "|" + "\033[0m"
            else:
                line_cells += cell_char + "\033[94m" + " " + "\033[0m"

            # South wall
            if south_closed:
                line_floor += "\033[94m" + "---+" + "\033[0m"
            else:
                line_floor += "\033[94m" + "   +" + "\033[0m"

        print(line_cells)
        print(line_floor)
