*This project has been created as part of the 42 curriculum by gabach, ibady.*

# ---- A-MAZE-ING ----

<details>
  <summary><h4>Description</h4></summary>

  ___

  + General description: <br>
  This project is a __maze generator and solver__. It is able to generate and solve as many different mazes as needed using multiple algorithms. It displays the process on a __MiniLibX graphical interface__ that allows the user to manipulate the program and make choices via buttons. It also uses a __MazeGenerator__ that can be imported as a standalone module to generate/solve mazes (but without the MiniLibX display).

</details>
<details>
  <summary><h4>Instructions</h4></summary>

  ___
  ### 1. Makefile
  + Install dependencies: <br>
  ```make install```<br>

  + Clean temporary files and caches: <br>
  ```make clean```<br>

  + Check flake8 and mypy norms: <br>
  ```make lint```<br>

  ### 2. Execution
  + Run the program: <br>
  ```make run```<br>

  + Run the program in debug mode:<br>
  ```make debug```<br>
  
</details>
<details>
  <summary><h4>Format</h4></summary>

  ___
  + Format of the config file: <br>
    PARAMETERS NEEDED:<br>
    - WIDTH : maze width (number of cells)                            // example: WIDTH=20
    - HEIGHT : maze height (number of rows)                           // example: HEIGHT=15
    - ENTRY : entry coordinates (x,y)                                 // example: ENTRY=0,0
    - EXIT : exit coordinates (x,y)                                   // example: EXIT=19,14
    - OUTPUT_FILE : output filename                                   // example: OUTPUT_FILE=maze.txt
    - PERFECT : is the maze perfect? (only one solution possible)     // example: PERFECT=True
    - SEED : for reproductibility of the maze                         // example: SEED=42 <br>
    All of the above parameters need to be present in the configuration file. The structure must be as follows:     "PARAM=value". You can add comments, but they must start with "#" to be properly ignored.<br> 
</details>
<details>
  <summary><h4>Algorithms</summary>

  ___
  ### 1. Generation algorithms
  + Wilson:<br>
    This algirithm work by defining a random cell as part of the final maze then from another random cell it is trying to join it by creating a random path. If the path makes a loop then it destroy the part of the path that made the loop and continue until it join the cell randomly selected. When the cell is joined it build the path found in the maze. Then select another random cell that hasn't been expored yet and apply the same rule of pathfinding as befor to join the existing part of the maze. It repeats it until there are no more unvisited cells. It creats a maze that is always perfect, meaning that each cell is linked to another one by one only path.
    I choose this algorithme, firstly because unlike some other algorithms this one doesn't have a pattern, also because it is one that is not optimized and hard to implement so I found that it would be a fun chalenge to make one that works well, and finally it was fun to watch it create a maze


  + Recursive backtracking:<br>
    This algorithm uses recursion (specifically backtracking) to generate a maze that is guaranteed to be perfect.<br>
    First, it initializes a maze that has all cells closed. It chooses a random entry point as a starting point if it is not defined, marking it as visited. It then iters through all its neighbors and if it finds one that hasn't been visited yet and is in the maze's bounds, it breaks the wall between the two cells and chooses this neighbor as the current cell.   When there are no more remaining neighbors available, it goes back the the previous cell that may still have neighbors to visit. The algorithm continues so until all cells have been visited, and returns the resulting maze.<br>
    I chose this algoritm because I usually struggle with recursion and backtracking, so I wanted to train to better comprehend how it works. And it also is an advantageous algorithm in terms of speed and optimization.<br>

  ### 2. Pathfinding algorithm
  + A*:<br>
    This algorithm uses two lists to store visited cells and cells to visit, as well as a heuristic calcul for the cost, effectively finding the shortest path between the entry and exit coordinates.<br>
    It starts at the entry point provided and adds it to the visited list. It then adds its viable neighbors (those who are accessible, i.e. when there aren't walls between them) to the list of cells to visit. Those cells to visit are going to be sorted by a heuristic function, that is to say a function that calculates the cost of each cell using a specific criterion. The criterion in question is the Manhattan distance, which is the sum of the distance between the cell and the entry point and the distance between the cell and the exit point. The cell with the least cost is the one that is going to be visited next. This process is repeated until the exit point is reached or all cells have been visited.<br>
    As all cells have a parent cell that indicates the previous cell (where we came from to arrive on this cell), it simply has to retrace its steps back to the entry point, then reverse the resulting list of cells to obtain the path found from the entry to the exit.<br>
    I chose this algorithm because I found it easy to understand and implement, and it is pretty effective and optimized. Also I liked its name haha xD<br>
</details>
<details>
  <summary><h4>Display Options</h4></summary>


  + Jump point search:<br>
    This algorithm work like A* but it has an optimisation that makes it "walk" in the same direction untile it crosses eather a wall or the exit, then if it crosses a wall it calculate the cost. So that means it makes less calcualtion that the original A*<br>


  ___
  ### Graphical Interface:
  The MiniLibX library for Python has been used to create a graphical interface for the maze generation display.<br>
  When you run the program, you start at the main menu, where you can choose to see the maze options, change configuration settings (defaults are the parameters of the config file given at the start of the program), or exit the window. If you click on the "maze" button, you can choose to generate a new maze using the algorithm of your choice, aswell as solve the maze, toggle whether or not the path is displayed, and change colors. Each action has its own menu and buttons for a better organisation and structure. Small animations were made for generation, pathfinding, and a specific secret color change ;).<br>
</details>
<details>
  <summary><h4>Code Reusability</h4></summary>

  ___
  ### Maze Generator:
  The mazegen-* module can be imported as a standalone module, and it can be used to generate and solve mazes. It doesn't use the MiniLibX library for a graphical display.<br>
  + Instantiation:<br>
    To use it properly, you first need to instantiate a MazeGenerator object, by passing it these parameters:<br>
    - maze size = a tuple of integers for maze width and maze height (in that order)
    - entry point = a tuple of integers that indicates the entry coordinates of the maze (x, y)
    - exit point = a tuple of integers that indicates the exit coordinates of the maze (x, y)
    - perfect (optional) = whether or not the maze needs to be perfect (defaults to True if not specified)
    - seed (optional) = make the maze reproductible via a certain seed (integer or None, defaults to None)<br>
    The generator will then use these provided parameters to generate mazes, although you can modify them using the setter functions:<br>
    - set_maze_sz(maze_sz: tuple[int, int])
    - set_entry_exit_coordinates(point: tuple[int, int], type: str)      // example: set_entry_exit_coordinates((0, 0), "entry")
    - set_perfect(is_perfect: bool)
    - set_seed(seed: int | None)<br>
    If the values given are not valid, the generator raises a ValueError with helpful error messages.<br>
  + Maze generation:<br>
    To generate a maze, you need to use the method generate_maze() (no parameters needed).<br>
    For example, for a generator called "maze_gen", you can call: maze_gen.generate_maze(). It will return a Maze object that has the following attributes:<br>
    - sz = the maze size (width, height)
    - width = the maze width
    -  height = the maze height
    - entry_point = the coordinates of the entry point
    - exit_point = the coordinates of the exit point
    - cells = all the cells in the maze (Cells objects)
    - gen_steps = a list of generation steps (all Cells modified one by one)
    - solving_steps = a list of solving steps (visited Cells in order)
    - path = a list of cells that correspond to the path (undefined if the maze has not been solved first)
    - path_dirs = a list of directions that correspond to the path (also not defined if not solved)
    - pattern_cells = a set of coordinates that form the 42 pattern in the middle of the maze<br>
  + Maze solving:<br>
    To access a solution for the maze, you need to use the method solve_maze() that takes a Maze object as parameter. It will modify directly the attributes "path" and "path_dirs" of the maze, respectively a list of Cells and a list of directions ("N", "S", "W", "E") that both indicate the path between the entry and exit.<br>
  + Maze Information:<br>
    You can also access the maze's information by calling the method write_to_output() that takes the name of the output file as parameter and writes in it the hexadecimal representation of the maze, then the entry/exit coordinates followed by a list of directions for the path.<br>
  + Algorithms used:<br>
    The algorithms used by default are the "rec_backtrack" = recursive backtracking (generation) and "jump_point_search" = jump point search (pathfinding), but should you wish to use other available algorithms instead (such as wilson or a* star), you can change directly the generator's attributes like so: "maze_gen.gen_algo = wilson" or "maze_gen.solve_algo = a_star".<br>
</details>
<details>
  <summary><h4>Team and Project Management</h4></summary>

  ___
  ### 1. Roles:
  + Gabach:<br>
    - wilson generation algorithm
    - jump point search pathfinding algorithm
    - project logic and construction
    - custom font for the graphical display
    - comments and docstrings
    - git repository structure and organisation
    - Makefile
    - menu image display<br>
  + Ibady:<br>
    - parsing
    - recursive backtracking generation algorithm
    - a* pathfinding algorithm
    - mlx graphical interface (buttons, animations...)
    - README<br>
  ### 2. Planning:
  We had initially planned to finish the project in about two weeks, and it took more like three weeks (mais c ok).<br>

  ### 3. Pros and Cons:
  We worked pretty well together, no conflicts of any sort, and we discussed how to implement things so as to disrupt what the other did as little as possible. We were also quite organised with the github branches and we used pull requests to approve/disapprove of the changes. Though we realized at some point during the project that we probably shoud have spent more time in the beginning stages of the project to establish a more defined structure and logic, because we ended up remaking a lot of things gradually as we had more ideas and problems to solve that popped up.<br>

  ### 4. Tools:
  We used an online visualization tool that shows how different generation and pathfinding algorithms work with animations (link in Resources section).<br>
</details>
<details>
  <summary><h4>Resources</h4></summary>

  ___
  ### 1. Links:
  For the MiniLibX library, we used the various MLX docs for C language as well as the source code:<br>
    - [MiniLibX | 42 Docs](https://harm-smits.github.io/42docs/libs/minilibx/)<br>
    - [MiniLibx Man Page](https://qst0.github.io/ft_libgfx/man_mlx.html)<br><br>
  For the algorithms:<br>
    - [Recursive Backtracking Algorithm](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)<br>
    - [Wilson Algorithm](https://medium.com/@batu.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76)<br>
    - [A* Algorithm](https://www.youtube.com/watch?v=-L-WgKMFuhE&t=2s)<br>
    - [Jump Point Search](https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search)<br>
    - [Maze Algorithms Visualization Tool](https://amazeing.app)<br>
  
  ### 2. AI Usage:
  ChatGPT was used a little bit, mostly for some explanations on how to handle the MiniLibX library, especially because of the lack of documentation for the Python version.<br>
</details>
