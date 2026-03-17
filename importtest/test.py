from mazegen import MazeGenerator, Maze, wilson


def main() -> None:

    mazegen: MazeGenerator = MazeGenerator(
        (20, 20),
        (0, 0),
        (19, 19)
    )

    maze: Maze = mazegen.generate_maze()
    mazegen.write_to_output(maze, "output.txt")
    mazegen.solve_maze(maze)

    mazegen.tui_display_maze(maze.maze_to_hexa())
    mazegen.tui_display_maze(
        maze.maze_to_hexa(),
        maze.path_dirs,
        maze.entry_point,
        maze.exit_point
    )

    mazegen.set_maze_sz((10, 10))
    mazegen.set_entry_exit_point((0, 1), "exit")
    mazegen.set_seed(42)

    maze = mazegen.generate_maze()
    mazegen.solve_maze(maze)

    mazegen.tui_display_maze(maze.maze_to_hexa())
    mazegen.tui_display_maze(
        maze.maze_to_hexa(),
        maze.path_dirs,
        maze.entry_point,
        maze.exit_point
    )

    maze = mazegen.generate_maze()
    mazegen.solve_maze(maze)

    mazegen.tui_display_maze(maze.maze_to_hexa())
    mazegen.tui_display_maze(
        maze.maze_to_hexa(),
        maze.path_dirs,
        maze.entry_point,
        maze.exit_point
    )
    mazegen.gen_algo = wilson
    maze = mazegen.generate_maze()
    mazegen.solve_maze(maze)

    mazegen.tui_display_maze(maze.maze_to_hexa())
    mazegen.tui_display_maze(
        maze.maze_to_hexa(),
        maze.path_dirs,
        maze.entry_point,
        maze.exit_point
    )


if __name__ == "__main__":

    main()
