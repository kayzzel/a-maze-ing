from .display_cell import DisplayCell
from ..utils.cleanup import clear_img
from .color_palette import RAINBOW_PALETTE, Colors
from .maze_generator import Maze
import time


class MazeDisplay:

    """

    ---- initializing the maze ----

    [parameters needed]

     => maze_input: the list of hexadecimal values for the cells
     => win_sz: the size of the window (width and height)
     => maze_sz: the size of the maze img (width and height)
     => mlx_data: the mlx object, the mlx pointer, and the mlx window
     => colors: the color palette containing all the colors
     => path:
            the list of letters that indicate the path
            + the entry/exit coordinates

    [attributes of the class]

     => maze_pos: the position of the maze inside the window
     => toggle_path:
            indicates whether or not the path needs to be displayed
     => generated: indicates whether or not the maze has been generated
     => path_displayed:
            indicates whether or not the path is currently displayed
     => path: a list of coordinates that form the path
     => coor: the entry/exit coordinates for the path
     => img: the maze image
     => cells: the list of individual cells
     => color_palette: the entire color palette
     => current_colors: the current colors of the maze
     => bg_color: the background color of the maze
     => animating: indicates whether or not the maze is currently animated
     => anim_row, anim_col: coordinates of the current cell to animate
     => frame_delay, frame_count: sets the animating speed

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

        clear_img(self.buf, self.img_height, self.sz_line)

        self.maze: Maze = maze

        self.generated = False

        self.cells: list[list[DisplayCell]] = []

        self.cell_sz: int = self.img_width // maze.width

        for row in range(maze.height):

            self.cells.append([])

            for col in range(maze.width):

                bg_color: tuple = self.bg_color

                if (col, row) in [
                    maze.entry_point,
                    maze.exit_point
                ]:

                    bg_color = self.entry_exit_color

                if (row, col) in self.maze.pattern_cells:

                    bg_color = self.wall_color

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

        self.img_pos: tuple[int, int] = (
            (self.win_sz[0] - self.img_sz[0]) // 2,
            self.win_sz[1] // 10
        )

    def start_animation(self) -> None:

        self.animating = True
        self.anim_step = 0

        if self.rainbow_mode:
            self.frame_delay = 0.00000000000001

        elif self.animating_path:
            self.frame_delay = 10 / len(self.maze.gen_steps) / 60
            self.cur_bg_color = (115, 115, 115, 255)
            self.steps: list = self.maze.solving_steps

        else:
            self.generated = False
            self.frame_delay = 10 / len(self.maze.gen_steps) / 60
            self.cur_bg_color = (115, 115, 115, 255)
            self.steps = self.maze.gen_steps

        self.frame_count = time.time()

    def stop_animation(self) -> None:

        self.generated = True
        self.animating = False

        if self.animating_path:
            self.toggle_path_on_off()

        self.animating_path = False
        self.change_colors([
            self.wall_color,
            self.bg_color,
            self.path_color,
            self.entry_exit_color
        ])

    def display_anim_step(self) -> None:

        if not self.animating:
            return None

        if self.anim_step == len(self.steps):
            self.stop_animation()
            return None

        if time.time() - self.frame_count < self.frame_delay:
            return None

        self.frame_count = time.time()

        if self.rainbow_mode and self.generated:
            self.rainbow_step()
            return None

        step_cell = self.steps[self.anim_step]
        cur_step_cell: DisplayCell = self.cells[step_cell.row][step_cell.col]

        cur_step_cell.walls = step_cell.walls

        if (step_cell.col, step_cell.row) not in [
            self.maze.entry_point,
            self.maze.exit_point
        ]:
            cur_step_cell.bg_color = (255, 0, 0, 255)

        cur_step_cell.draw_cell()

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

        if self.anim_step == len(self.steps):
            cur_step_cell.bg_color = self.cur_bg_color
            cur_step_cell.draw_cell()

    def draw(self) -> None:

        for row in self.cells:

            for cell in row:

                cell.draw_cell()

    def display_on_window(self) -> None:

        if not self.animating and not self.generated:
            return None

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.img_pos
        )

    """

    toggles path on and off
    animates the path display if it has not yet been displayed

    """
    def toggle_path_on_off(self, animated_display: bool = False) -> None:

        # checks if the maze has been generated

        if not self.generated:
            return None

        # checks if animation is needed

        if animated_display:

            self.animating_path = True
            self.start_animation()
            return None

        self.animating_path = False
        self.toggle_path = not (self.toggle_path)
        self.cur_bg_color = (
            self.path_color if self.toggle_path
            else self.bg_color
        )

        # redrawing the maze to display/remove the path

        for path_col, path_row in self.maze.path:

            if (path_col, path_row) not in [
                self.maze.entry_point,
                self.maze.exit_point
            ]:

                self.cells[path_row][path_col].wall_color = self.wall_color
                self.cells[path_row][path_col].bg_color = self.cur_bg_color
                self.cells[path_row][path_col].draw_cell()

        # uncomment the floowing line
        # if you want to animate the path display every time it is toggled on

        # self.path_displayed = not (self.path_displayed)

    """

    changes the colors of the maze
    chooses a set of colors randomly in the color palette

    """

    def change_colors(self, new_colors: list[tuple]) -> None:

        # checks if the maze has been generated

        if not self.generated:
            return None

        # sets the new colors

        self.wall_color = new_colors[0]
        self.bg_color = new_colors[1]
        self.path_color = new_colors[2]
        self.entry_exit_color = new_colors[3]

        clear_img(self.buf, self.img_height, self.sz_line)

        # changes the colors of each cell in the maze then redraws it

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

        if not self.generated:
            return None

        self.rainbow_mode = not (self.rainbow_mode)

        self.rainbow_delimiter: int = (
            self.maze.width // len(self.rainbow_palette)
        )

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

        for row in self.cells:

            cur_color_index: int = 0
            rainbow_palette_index: int = 0

            for cell in row:

                if cur_color_index == self.rainbow_delimiter:
                    cur_color_index = 0
                    rainbow_palette_index += 1
                    if rainbow_palette_index == len(self.rainbow_palette):
                        rainbow_palette_index = 0

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

        last_color: Colors = self.rainbow_palette[-1]
        self.rainbow_palette.remove(self.rainbow_palette[-1])
        self.rainbow_palette = [last_color] + self.rainbow_palette

    """

    clears the maze image then destroys it (cleanup)

    """

    def clean_img(self) -> None:

        clear_img(self.buf, self.img_height, self.sz_line)

        self.mlx.mlx_destroy_image(
            self.mlx_ptr,
            self.img
        )
