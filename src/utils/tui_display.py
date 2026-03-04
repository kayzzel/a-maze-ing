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
