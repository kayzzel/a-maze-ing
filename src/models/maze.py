from .cell import Cell
from ..utils import clear_img
from ..utils import get_rainbow_palette
from enum import Enum
import random
import time


class Walls(str, Enum):

    NORTH = "13579BDFbdf"
    SOUTH = "4567CDEFcdef"
    EAST = "2367BEFbefAa"
    WEST = "89BCDEFbcdefAa"


class Maze:

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
        maze_input: list[str],
        win_sz: tuple[int, int],
        maze_sz: tuple[int, int],
        mlx_data: tuple,
        colors: list[list[tuple[int, int, int, int]]],
        path: tuple
    ) -> None:

        if not all(
            (
                hexa in "0123456789BCDEFbcdefAa"
                and len(maze_row) == len(maze_input[0])
            )
            for maze_row in maze_input
            for hexa in maze_row
        ) or not self.check_if_maze_closed(maze_input):

            raise ValueError("Invalid input for the maze's cells!")

        self.input: list[str] = maze_input
        self.width, self.height = maze_sz
        self.maze_pos: tuple[int, int] = (
            (win_sz[0] - self.width) // 2,
            (win_sz[1] - self.height - 100) // 2
        )
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.toggle_path: bool = False
        self.generated: bool = False
        self.path_displayed: bool = False
        self.coor: tuple = path[1]
        self.path: list[tuple] = self.parse_path(path[0])
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )
        self.buf, self.bpp, self.sz_line, *oth = (
            self.mlx.mlx_get_data_addr(self.img)
        )
        self.cells: list[list] = [
            [None for _ in range(len(self.input[0]))]
            for _ in range(len(self.input))
        ]
        self.color_palette: list[list[tuple[int, int, int, int]]] = colors
        self.current_colors: list[
            tuple[int, int, int, int]
        ] = random.choice(self.color_palette)
        self.bg_color: int = 1
        self.animating: bool = False
        self.anim_row: int = 0
        self.anim_col: int = 0
        self.frame_delay: float = 0.0000001
        self.frame_count: float = 0
        self.animating_speed: int = len(maze_input) // 10
        self.rainbow_mode: bool = False
        self.rainbow_palette: list[
            list[tuple[int, int, int, int]]
        ] = get_rainbow_palette()
        self.rainbow_delimiter: int = (
            len(self.input[0]) // len(self.rainbow_palette)
        )

    """

    checks whether or not the maze is properly closed on all sides

    """

    @staticmethod
    def check_if_maze_closed(maze_input: list[str]) -> bool:

        if not all(hexa_val in Walls.NORTH for hexa_val in maze_input[0]):
            return False

        if not all(hexa_val in Walls.SOUTH for hexa_val in maze_input[-1]):
            return False

        if not all(hexa_val in Walls.WEST for hexa_val in [
            hexa_line[0] for hexa_line in maze_input
        ]):
            return False

        if not all(hexa_val in Walls.EAST for hexa_val in [
            hexa_line[-1] for hexa_line in maze_input
        ]):
            return False

        return True

    """

    starts the animation for displaying the maze/path

    """
    def start_animation(self) -> None:

        # clearing the entire maze
        # only if the path is not displayed or needs to be

        if not self.toggle_path or self.path_displayed:

            clear_img(self.buf, self.height, self.sz_line)
            self.toggle_path = False
            self.path_displayed = False
            self.generated = False
            self.bg_color = 1
            self.frame_delay = 0.0000001
            self.animating_speed = len(self.input) // 10
            self.cells = [
                [None for _ in range(len(self.input[0]))]
                for _ in range(len(self.input))
            ]

        # reinitializing the animation parameters to zero

        self.anim_row = 0
        self.anim_col = 0
        self.animating = True
        self.frame_count = time.monotonic()

    """

    a single animation step (one cell)
    called by the global update function each turn

    """

    def animate_step(self) -> None:

        if not self.animating:
            return None

        # doesn't draw the cell if not yet arrived at the frame delay

        if time.monotonic() - self.frame_count < self.frame_delay:
            return None

        # resets the frame count for next cell

        self.frame_count = time.monotonic()

        if self.rainbow_mode and self.generated:
            self.rainbow_step()
            return None

        # checks if at the end of the maze

        for _ in range(self.animating_speed):

            if self.anim_row >= len(self.input):
                self.animating = False
                self.generated = True
                return None

            # checks if the path needs to be displayed

            if self.toggle_path and self.path:

                # checks if arrived at the end of the path

                if self.cur_path_pos >= len(self.path):
                    self.generated = True
                    self.path_displayed = True
                    return None

                # gets the cell coordinates from the path

                self.anim_row, self.anim_col = self.path[
                    self.cur_path_pos
                ]

                # going to the next cell in the path

                self.cur_path_pos += 1

            # initializing the cell

            self.cells[self.anim_row][self.anim_col] = Cell(
                self.input[self.anim_row][self.anim_col],
                (self.anim_col, self.anim_row),
                self.width // len(self.input[0]),
                (self.buf, self.sz_line, self.bpp),
                (
                    self.current_colors[0],
                    self.current_colors[self.bg_color]
                )
            )

            self.cells[self.anim_row][self.anim_col].draw()

            # going to the next cell

            if not self.toggle_path:

                self.anim_col += 1
                if self.anim_col >= len(self.input[0]):
                    self.anim_col = 0
                    self.anim_row += 1

    """

    toggles path on and off
    animates the path display if it has not yet been displayed

    """
    def toggle_path_on_off(self) -> None:

        # checks if the maze has been generated

        if not self.generated:
            return None

        self.toggle_path = not (self.toggle_path)
        self.bg_color = (
            2 if self.toggle_path
            else 1
        )

        # checks if animation is needed

        if self.toggle_path and not self.path_displayed:

            self.cur_path_pos: int = 0
            self.frame_delay = 0.01
            self.animating_speed = 1
            self.start_animation()
            self.path_displayed = True

            return None

        # redrawing the maze to display/remove the path

        for path_row, path_col in self.path:

            self.cells[path_row][path_col].colors = (
                self.current_colors[0],
                self.current_colors[self.bg_color]
            )
            self.cells[path_row][path_col].draw()

        # uncomment the floowing line
        # if you want to animate the path display every time it is toggled on

        # self.path_displayed = not (self.path_displayed)

    """

    changes the colors of the maze
    chooses a set of colors randomly in the color palette

    """

    def change_colors(self) -> None:

        # checks if the maze has been generated

        if not self.generated:
            return None

        if self.rainbow_mode:
            self.activate_rainbow()

        # sets the new colors

        new_colors: list[
            tuple[int, int, int, int]
        ] = random.choice(self.color_palette)

        while (
            new_colors == self.current_colors
            and len(self.color_palette) > 1
        ):
            new_colors = random.choice(self.color_palette)

        self.current_colors = new_colors

        # changes the colors of each cell in the maze then redraws it

        for row in range(len(self.input)):

            for col in range(len(self.input[0])):

                self.bg_color = 1

                if self.toggle_path and (row, col) in self.path:
                    self.bg_color = 2

                self.cells[row][col].colors = (
                    self.current_colors[0],
                    self.current_colors[self.bg_color]
                )
                self.cells[row][col].draw()

    def activate_rainbow(self) -> None:

        if not self.generated:
            return None

        self.rainbow_mode = not (self.rainbow_mode)

        if not self.rainbow_mode or self.rainbow_delimiter < 1:
            self.animating = False
            self.frame_delay = 0.0000001
            self.change_colors()
            return None

        self.animating = True
        self.frame_delay = 0.00000000001
        self.frame_count = time.monotonic()

    def rainbow_step(self) -> None:

        for row in range(len(self.input)):

            cur_color_index: int = 0
            rainbow_palette_index: int = 0

            for col in range(len(self.input[0])):

                if cur_color_index == self.rainbow_delimiter:
                    cur_color_index = 0
                    rainbow_palette_index += 1
                    if rainbow_palette_index == len(self.rainbow_palette):
                        rainbow_palette_index = 0

                self.bg_color = 1

                if self.toggle_path and (row, col) in self.path:
                    self.bg_color = 2

                self.cells[row][col].colors = (
                    self.rainbow_palette[rainbow_palette_index][0],
                    self.rainbow_palette[rainbow_palette_index][self.bg_color]
                )

                cur_color_index += 1

                self.cells[row][col].draw()

        last_color: list[tuple[int, int, int, int]] = self.rainbow_palette[-1]
        self.rainbow_palette.remove(self.rainbow_palette[-1])
        self.rainbow_palette = [last_color] + self.rainbow_palette

    """

    parses the list of letters indicating directions
    returns a list of cell coordinates in the correct order

    """

    def parse_path(self, path: str) -> list[tuple]:

        if not path:
            return []

        # setting the indexes to the entry coordinates

        row, col = self.coor[0]
        path_coor: list[tuple] = [(row, col)]

        # moves the indexes based on the direction (north, south, east, west)

        for p in path:

            match p:

                case "N":
                    row -= 1
                case "S":
                    row += 1
                case "W":
                    col -= 1
                case "E":
                    col += 1
                case _:
                    print("Invalid path provided!")
                    return []

            # checks if the indexes don't go out of the maze

            if (
                not (0 <= row < len(self.input))
                or not (0 <= col < len(self.input[0]))
            ):
                print("Invalid path provided!")
                return []

            path_coor.append((row, col))

        # checks if following the directions does lead to the exit coordinates

        if (col, row) != self.coor[1]:
            print("Invalid path provided!")
            return []

        return path_coor

    """

    clears the maze image then destroys it (cleanup)

    """

    def clean_img(self) -> None:

        clear_img(self.buf, self.height, self.sz_line)

        self.mlx.mlx_destroy_image(
            self.mlx_ptr,
            self.img
        )
