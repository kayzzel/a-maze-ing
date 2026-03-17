*This project has been created as part of the 42 curriculum by gabach, ibady.*

# ---- MAZE GENERATOR ----

  ___
  The mazegen module allows the user to generate and solve mazes. It doesn't provide a graphical display, but a terminal display is available.<br><br>
  ### Instantiation<br><br>
  To use it properly, you first need to instantiate a MazeGenerator object, by passing it these parameters:<br><br>
      - maze size = a tuple of integers for maze width and maze height (in that order)<br>
      - entry point = a tuple of integers that indicates the entry coordinates of the maze (x, y)<br>
      - exit point = a tuple of integers that indicates the exit coordinates of the maze (x, y)<br>
      - perfect (optional) = whether or not the maze needs to be perfect (defaults to True if not specified)<br>
      - seed (optional) = make the maze reproductible via a certain seed (integer or None, defaults to None)<br><br>
  
  The generator will then use these provided parameters to generate mazes, although you can modify them using the setter functions:<br><br>
      - set_maze_sz(maze_sz: tuple[int, int])<br>
      - set_entry_exit_coordinates(point: tuple[int, int], type: str)<br>
    => Example: set_entry_exit_coordinates((0, 0), "entry")<br>
      - set_perfect(is_perfect: bool)<br>
      - set_seed(seed: int | None)<br><br>
  
  If the values given are not valid, the generator raises a ValueError with helpful error messages.<br><br>
  ### Maze generation<br><br>
  To generate a maze, you need to use the method generate_maze() (no parameters needed).<br><br>
  For example, for a generator called "maze_gen", you can call: maze_gen.generate_maze(). It will return a Maze object that has the following attributes:<br><br>
      - sz = the maze size (width, height)<br>
      - width = the maze width<br>
      -  height = the maze height<br>
      - entry_point = the coordinates of the entry point<br>
      - exit_point = the coordinates of the exit point<br>
      - cells = all the cells in the maze (Cells objects)<br>
      - gen_steps = a list of generation steps (all Cells modified one by one)<br>
      - solving_steps = a list of solving steps (visited Cells in order)<br>
      - path = a list of cells that correspond to the path (undefined if the maze has not been solved first)<br>
      - path_dirs = a list of directions that correspond to the path (also not defined if not solved)<br>
      - pattern_cells = a set of coordinates that form the 42 pattern in the middle of the maze<br><br>
  ### Maze solving<br><br>
  To access a solution for the maze, you need to use the method solve_maze() that takes a Maze object as parameter. It will modify directly the attributes "path" and "path_dirs" of the maze, respectively a list of Cells and a list of directions ("N", "S", "W", "E") that both indicate the path between the entry and exit.<br><br>
  ### Maze Information:<br><br>
  You can also access the maze's information by calling the method write_to_output() that takes the name of the output file as parameter and writes in it the hexadecimal representation of the maze, then the entry/exit coordinates followed by a list of directions for the path.<br><br>
  ### Maze Display<br><br>
  You can have a visual representation of the maze in the terminal by calling the method tui_display_maze().<br>
  If you wish to see only the maze's structure, you should pass it only the hexadecimal representation of the maze as a parameter (that you can obtain with the maze_to_hexa() method of the Maze object). If you wish to see the solution as well, you should call it with three more parameters: the path in string representation (the path_dirs attribute of the Maze object if it has been solved), the entry coordinates and the exit coordinates.<br><br>
  ### Algorithms used<br><br>
  The algorithms used by default are the "rec_backtrack" = recursive backtracking (generation) and "a_star" = A* (pathfinding), but should you wish to use other available algorithms instead (such as wilson or jump point search), you can use the generator's setter functions set_gen_algo() and set_solve_algo() like so: "maze_gen.set_gen_algo(wilson)" or "maze_gen.set_solve_algo(jump_point_search)".<br><br>
