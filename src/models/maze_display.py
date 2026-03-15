from .display_cell import DisplayCell
from ..utils.cleanup import clear_img
from .color_palette import RAINBOW_PALETTE, Colors
from .maze_generator import Maze
import time


class MazeDisplay:
    """
        Description:
    Manages the visual rendering of a maze onto an MLX image. Handles
    cell drawing, generation and path animations, color changes, rainbow
    mode, and displaying the final image in the window

        Parameters:
    img_sz -> the size of the maze image as (width, height)
    win_sz -> the size of the window as (width, height)
    mlx_data -> a tuple containing (mlx, mlx_ptr, mlx_win) for the MLX instance

        Attributes:
    img_sz, img_width, img_height -> maze image dimensions
    win_sz -> the window size
    mlx, mlx_ptr, mlx_win -> the MLX rendering context
    wall_color -> the RGBA color used for walls
    bg_color -> the RGBA color used for the cell background
    path_color -> the RGBA color used for the solution path
    entry_exit_color -> the RGBA color used for entry and exit cells
    generated -> True once maze generation is complete
    animating -> True while a generation or path animation is running
    animating_path -> True while the path solving animation is running
    anim_step -> the index of the current animation frame
    frame_count -> the timestamp of the last rendered frame
    frame_delay -> the minimum time in seconds between frames
    toggle_path -> True if the solution path is currently displayed
    rainbow_palette -> the ordered list of Colors used in rainbow mode
    rainbow_mode -> True while rainbow mode is active
    maze -> the Maze instance currently being displayed
    cells -> the 2D grid of DisplayCell instances
    cell_sz -> the pixel size of each cell
    img -> the MLX image used to render the maze
    buf, bpp, sz_line -> the raw image buffer and its parameters
    img_data -> the image buffer packed as (buf, sz_line, bpp)
    img_pos -> the (x, y) position of the maze image in the window
    """

    def __init__(
        self,
        img_sz: tuple[int, int],
        win_sz: tuple[int, int],
        mlx_data: tuple
    ) -> None:

        self.img_sz: tuple[int, int] = img_sz
        self.img_width: int = img_sz[0]
        self.img_height: int = img_sz[1]
        self.win_sz: tuple[int, int] = win_sz
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data

        # Default color scheme:
        # white walls, black background, blue path, green entry/exit
        self.wall_color: tuple = (255, 255, 255, 255)
        self.bg_color: tuple = (0, 0, 0, 255)
        self.path_color: tuple = (0, 0, 255, 255)
        self.entry_exit_color: tuple = (0, 255, 0, 255)

        self.initialize_img()

        self.generated: bool = False
        self.animating: bool = False
        self.animating_path: bool = False
        self.anim_step: int = 0
        self.frame_count: float = 0
        self.frame_delay: float = 0
        self.toggle_path: bool = False

        self.rainbow_palette: list[Colors] = RAINBOW_PALETTE
        self.rainbow_mode: bool = False

    def set_new_maze(self, maze: Maze) -> None:
        """
            Description:
        Load a new maze, clear the image buffer, and build the 2D grid of
        DisplayCells. Each cell is drawn with all walls closed initially,
        and entry, exit, and pattern cells are given their designated colors

            Parameters:
        maze -> the Maze instance to load and display
        """

        clear_img(self.buf, self.img_height, self.sz_line)

        self.maze: Maze = maze
        self.generated = False
        self.cells: list[list[DisplayCell]] = []
        self.cell_sz: int = self.img_width // maze.width

        for row in range(maze.height):

            self.cells.append([])

            for col in range(maze.width):

                # Determine the background color for this cell
                bg_color: tuple = self.bg_color

                if (col, row) in [
                    maze.entry_point,
                    maze.exit_point
                ]:
                    bg_color = self.entry_exit_color

                if (row, col) in self.maze.pattern_cells:
                    bg_color = self.wall_color

                # Create the cell with all walls closed,
                # then sync its wall state
                self.cells[row].append(DisplayCell(
                    (col, row),
                    self.cell_sz,
                    self.img_data,
                    [self.wall_color, bg_color],
                    {"N": True, "S": True, "W": True, "E": True}
                ))

                self.cells[row][col].draw_cell()

                self.cells[row][col].walls = self.maze.cells[row][col].walls

    def initialize_img(self) -> None:
        """
            Description:
        Allocate the MLX image used to render the maze, retrieve its buffer,
        clear it, and compute the centered position of the image within
        the window
        """

        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            *self.img_sz
        )
        self.buf, self.bpp, self.sz_line, _ = (
            self.mlx.mlx_get_data_addr(self.img)
        )
        self.img_data: tuple[memoryview, int, int] = (
            self.buf, self.sz_line, self.bpp
        )
        clear_img(self.buf, self.img_height, self.sz_line)

        # Center the maze image horizontally and place it near the top
        self.img_pos: tuple[int, int] = (
            (self.win_sz[0] - self.img_sz[0]) // 2,
            self.win_sz[1] // 10
        )

    def start_animation(self) -> None:
        """
            Description:
        Begin an animation by resetting the step counter and computing the
        frame delay based on the number of steps. Sets up the appropriate
        step list depending on whether a path or generation animation is
        starting, and records the current time as the first frame timestamp
        """

        self.animating = True
        self.anim_step = 0

        if self.rainbow_mode:
            # Rainbow mode runs as fast as possible
            self.frame_delay = 0.00000000000001

        elif self.animating_path:
            # Scale the delay so the path animation lasts around 10 seconds
            self.frame_delay = 10 / len(self.maze.gen_steps) / 60
            self.cur_bg_color = (115, 115, 115, 255)
            self.steps: list = self.maze.solving_steps

        else:
            # Scale the delay so the generation animation
            # lasts around 10 seconds
            self.generated = False
            self.frame_delay = 10 / len(self.maze.gen_steps) / 60
            self.cur_bg_color = (115, 115, 115, 255)
            self.steps = self.maze.gen_steps

        self.frame_count = time.time()

    def stop_animation(self) -> None:
        """
            Description:
        Stop the current animation and mark the maze as fully generated.
        If a path animation was running, toggle the path display off and
        restore all maze colors to their current settings
        """

        self.generated = True
        self.animating = False

        # If the path animation just ended, toggle the path off cleanly
        if self.animating_path:
            self.toggle_path_on_off()

        self.animating_path = False

        # Restore the maze to its current color settings
        self.change_colors([
            self.wall_color,
            self.bg_color,
            self.path_color,
            self.entry_exit_color
        ])

    def display_anim_step(self) -> None:
        """
            Description:
        Advance the animation by one step if the frame delay has elapsed.
        Highlights the current step cell in red and restores the previous
        step cell to the background color. Stops the animation automatically
        when all steps have been displayed. In rainbow mode, delegates to
        rainbow_step instead
        """

        if not self.animating:
            return None

        # Check if all steps have been displayed
        if self.anim_step == len(self.steps):
            self.stop_animation()
            return None

        # Wait until the next frame is due
        if time.time() - self.frame_count < self.frame_delay:
            return None

        self.frame_count = time.time()

        # Delegate to rainbow_step if rainbow mode is active
        if self.rainbow_mode and self.generated:
            self.rainbow_step()
            return None

        # Highlight the current step cell in red
        step_cell = self.steps[self.anim_step]
        cur_step_cell: DisplayCell = self.cells[step_cell.row][step_cell.col]
        cur_step_cell.walls = step_cell.walls

        if (step_cell.col, step_cell.row) not in [
            self.maze.entry_point,
            self.maze.exit_point
        ]:
            cur_step_cell.bg_color = (255, 0, 0, 255)

        cur_step_cell.draw_cell()

        # Restore the previous step cell to the background color
        if self.anim_step > 0:

            prev_cell = self.steps[self.anim_step - 1]

            if (prev_cell.col, prev_cell.row) not in [
                self.maze.entry_point,
                self.maze.exit_point
            ]:
                self.cells[prev_cell.row][prev_cell.col].bg_color = (
                    self.cur_bg_color
                )

            self.cells[prev_cell.row][prev_cell.col].draw_cell()

        self.anim_step += 1

        # Restore the last cell once all steps are done
        if self.anim_step == len(self.steps):
            cur_step_cell.bg_color = self.cur_bg_color
            cur_step_cell.draw_cell()

    def draw(self) -> None:
        """
            Description:
        Redraw every cell in the maze grid onto the image buffer
        """

        for row in self.cells:

            for cell in row:

                cell.draw_cell()

    def display_on_window(self) -> None:
        """
            Description:
        Render the maze image onto the window at its configured position.
        Does nothing if the maze is neither animating nor fully generated
        """

        if not self.animating and not self.generated:
            return None

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.img_pos
        )

    def toggle_path_on_off(self, animated_display: bool = False) -> None:
        """
            Description:
        Show or hide the solution path on the maze. If animated_display is
        True, the path is revealed via an animation instead of instantly.
        Does nothing if the maze has not been generated yet

            Parameters:
        animated_display -> if True, start a path animation instead of
                            toggling instantly (default False)
        """

        # Do nothing if the maze has not been generated yet
        if not self.generated:
            return None

        # Start a path animation if requested
        if animated_display:
            self.animating_path = True
            self.start_animation()
            return None

        self.animating_path = False
        self.toggle_path = not (self.toggle_path)

        # Use the path color when showing, background color when hiding
        self.cur_bg_color = (
            self.path_color if self.toggle_path
            else self.bg_color
        )

        # Redraw path cells with the updated background color
        for path_col, path_row in self.maze.path:

            if (path_col, path_row) not in [
                self.maze.entry_point,
                self.maze.exit_point
            ]:

                self.cells[path_row][path_col].wall_color = self.wall_color
                self.cells[path_row][path_col].bg_color = self.cur_bg_color
                self.cells[path_row][path_col].draw_cell()

        # uncomment the following line
        # if you want to animate the path display every time it is toggled on

        # self.path_displayed = not (self.path_displayed)

    def change_colors(self, new_colors: list[tuple]) -> None:
        """
            Description:
        Apply a new set of colors to the maze and redraw every cell.
        Entry/exit, path, and pattern cells each receive their designated
        color. Does nothing if the maze has not been generated yet

            Parameters:
        new_colors -> a list of four RGBA tuples in the order
                      [wall_color, bg_color, path_color, entry_exit_color]
        """

        # Do nothing if the maze has not been generated yet
        if not self.generated:
            return None

        # Store the new color values
        self.wall_color = new_colors[0]
        self.bg_color = new_colors[1]
        self.path_color = new_colors[2]
        self.entry_exit_color = new_colors[3]

        clear_img(self.buf, self.img_height, self.sz_line)

        # Recolor and redraw each cell according to its role in the maze
        for row in range(self.maze.height):

            for col in range(self.maze.width):

                cur_cell: DisplayCell = self.cells[row][col]

                bg_color: tuple = self.bg_color

                if (col, row) in [
                    self.maze.entry_point,
                    self.maze.exit_point
                ]:
                    bg_color = self.entry_exit_color

                elif self.toggle_path and (col, row) in self.maze.path:
                    bg_color = self.path_color

                elif (row, col) in self.maze.pattern_cells:
                    bg_color = self.wall_color

                cur_cell.wall_color = self.wall_color
                cur_cell.bg_color = bg_color
                cur_cell.draw_cell()

    def activate_rainbow(self) -> None:
        """
            Description:
        Toggle rainbow mode on or off. When enabled, starts the rainbow
        animation. When disabled, or if the maze is too narrow to display
        all palette colors, stops the animation and restores the current
        colors. Does nothing if the maze has not been generated yet
        """

        if not self.generated:
            return None

        self.rainbow_mode = not (self.rainbow_mode)

        # Compute how many columns each color band spans
        self.rainbow_delimiter: int = (
            self.maze.width // len(self.rainbow_palette)
        )

        # Disable rainbow mode if it was turned off or the maze is too narrow
        if not self.rainbow_mode or self.rainbow_delimiter < 1:
            self.stop_animation()
            self.change_colors([
                self.wall_color,
                self.bg_color,
                self.path_color,
                self.entry_exit_color
            ])
            return None

        self.start_animation()

    def rainbow_step(self) -> None:
        """
            Description:
        Render one frame of the rainbow animation by assigning each cell
        a color from the rainbow palette based on its column position.
        At the end of each frame the palette is rotated by one position
        so the colors shift across the maze on the next frame.
        Entry/exit, path, and pattern cells use specific palette shades
        """

        for row in self.cells:

            cur_color_index: int = 0
            rainbow_palette_index: int = 0

            for cell in row:

                # Advance to the next palette color after each band of columns
                if cur_color_index == self.rainbow_delimiter:
                    cur_color_index = 0
                    rainbow_palette_index += 1
                    if rainbow_palette_index == len(self.rainbow_palette):
                        rainbow_palette_index = 0

                # Select the shade index based on the cell's role:
                # 0 = darkest (pattern), 1 = medium (background),
                # 2 = bright (path), 3 = light (entry/exit)
                bg_color: int = 1

                if self.toggle_path and (cell.col, cell.row) in self.maze.path:
                    bg_color = 2

                elif (cell.col, cell.row) in [
                    self.maze.entry_point,
                    self.maze.exit_point
                ]:
                    bg_color = 3

                elif (cell.row, cell.col) in self.maze.pattern_cells:
                    bg_color = 0

                cell.wall_color = self.rainbow_palette[
                    rainbow_palette_index
                ][0]
                cell.bg_color = self.rainbow_palette[
                    rainbow_palette_index
                ][bg_color]

                cell.draw_cell()

                cur_color_index += 1

        # Rotate the palette by moving the last color to the front
        last_color: Colors = self.rainbow_palette[-1]
        self.rainbow_palette.remove(self.rainbow_palette[-1])
        self.rainbow_palette = [last_color] + self.rainbow_palette

    def clean_img(self) -> None:
        """
            Description:
        Clear the maze image buffer and destroy the MLX image to free
        the associated memory. Should be called before closing the window
        """

        clear_img(self.buf, self.img_height, self.sz_line)

        self.mlx.mlx_destroy_image(
            self.mlx_ptr,
            self.img
        )
