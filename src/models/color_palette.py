from enum import Enum
from ..utils.cleanup import clear_img
from ..utils.mlx_display import img_put_px, draw_borders


Color_type = tuple[
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        ]


class Colors(Color_type, Enum):
    """
        Description:
    An enumeration of all available color families. Each member holds
    four RGBA tuples representing shades from darkest to lightest,
    used to populate the color palette and drive the rainbow mode

        Attributes:
    RED, ORANGE, YELLOW, GREEN_1, GREEN_2, BLUE_1, BLUE_2,
    VIOLET, PINK, GREY -> each holds four (R, G, B, A) tuples
                          ordered from dark to light
    """

    RED = (
        (79, 20, 14, 255),
        (115, 29, 20, 255),
        (176, 50, 33, 255),
        (212, 88, 76, 255)
    )
    ORANGE = (
        (102, 49, 16, 255),
        (138, 64, 22, 255),
        (181, 81, 24, 255),
        (227, 126, 70, 255)
    )
    YELLOW = (
        (94, 74, 10, 255),
        (130, 104, 18, 255),
        (171, 136, 21, 255),
        (214, 181, 71, 255)
    )
    GREEN_1 = (
        (38, 56, 10, 255),
        (68, 99, 19, 255),
        (104, 145, 28, 255),
        (163, 201, 85, 255)
    )
    GREEN_2 = (
        (12, 69, 21, 255),
        (20, 122, 35, 255),
        (28, 173, 51, 255),
        (74, 224, 98, 255)
    )
    BLUE_1 = (
        (15, 84, 78, 255),
        (23, 128, 119, 255),
        (33, 173, 163, 255),
        (76, 224, 213, 255)
    )
    BLUE_2 = (
        (15, 51, 84, 255),
        (25, 80, 128, 255),
        (38, 114, 181, 255),
        (91, 166, 227, 255)
    )
    VIOLET = (
        (40, 12, 74, 255),
        (73, 21, 122, 255),
        (105, 31, 173, 255),
        (174, 128, 217, 255)
    )
    PINK = (
        (99, 21, 56, 255),
        (148, 33, 83, 255),
        (184, 50, 108, 255),
        (222, 100, 152, 255)
    )
    GREY = (
        (0, 0, 0, 255),
        (61, 58, 58, 255),
        (138, 129, 129, 255),
        (255, 255, 255, 255)
    )


class Color:
    """
        Description:
    A wrapper around a Colors enum member that exposes its four
    shades as named attributes for convenient access

        Parameters:
    colors -> a Colors enum member containing four RGBA shades

        Attributes:
    dark -> the darkest shade of the color
    medium -> the medium-dark shade of the color
    bright -> the medium-light shade of the color
    light -> the lightest shade of the color
    nuances -> the original Colors enum member holding all four shades
    """

    def __init__(
        self,
        colors: Colors
    ) -> None:

        self.dark: tuple = colors[0]
        self.medium: tuple = colors[1]
        self.bright: tuple = colors[2]
        self.light: tuple = colors[3]
        self.nuances: Colors = colors


class ColorPalette:
    """
        Description:
    A visual color picker widget that renders a grid of color swatches
    onto an MLX image. Each column represents a color family and each
    row a shade, from darkest to lightest. The user can click a swatch
    to select a color

        Parameters:
    mlx_data -> a tuple containing (mlx, mlx_ptr, mlx_win) for the MLX instance
    win_sz -> the size of the window as (width, height)

        Attributes:
    colors -> the list of Color instances displayed in the palette
    mlx, mlx_ptr, mlx_win -> the MLX rendering context
    width -> the pixel width of the palette image
    height -> the pixel height of the palette image
    win_pos -> the (x, y) position of the palette in the window
    end_pos -> the (x, y) bottom-right corner of the palette in the window
    img -> the MLX image used to render the palette
    buf, bpp, sz_line -> the raw image buffer and its parameters
    column_width -> the pixel width of each color column
    row_height -> the pixel height of each shade row
    color_picked -> the RGBA tuple of the most recently selected color
    """

    def __init__(self, mlx_data: tuple, win_sz: tuple) -> None:

        # Build the list of Color wrappers for every color family
        self.colors: list[Color] = [
            Color(Colors.RED),
            Color(Colors.ORANGE),
            Color(Colors.YELLOW),
            Color(Colors.GREEN_1),
            Color(Colors.GREEN_2),
            Color(Colors.BLUE_1),
            Color(Colors.BLUE_2),
            Color(Colors.VIOLET),
            Color(Colors.PINK),
            Color(Colors.GREY)
        ]

        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data

        # Size the palette relative to the window, leaving room for borders
        self.width: int = win_sz[0] // 2 + 4
        self.height: int = win_sz[1] // 5 + 4

        # Position the palette near the bottom-left of the window
        self.win_pos: tuple[int, int] = (
            200,
            win_sz[1] - self.height - 50
        )
        self.end_pos: tuple[int, int] = (
            self.win_pos[0] + self.width,
            self.win_pos[1] + self.height
        )

        # Allocate the MLX image and get its buffer
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )

        self.buf, self.bpp, self.sz_line, _ = self.mlx.mlx_get_data_addr(
            self.img
        )

        clear_img(self.buf, self.height, self.sz_line)

        # Draw a 2-pixel white border around the palette
        draw_borders(
            (0, 0),
            (self.width, self.height),
            2,
            (self.buf, self.sz_line, self.bpp),
            (255, 255, 255, 255)
        )

        # Compute the cell dimensions from the drawable area inside the border
        self.column_width: int = (self.width - 4) // len(self.colors)
        self.row_height: int = (self.height - 4) // len(self.colors[0].nuances)

        self.draw_color_palette()

        # Default selected color is black
        self.color_picked: tuple[int, int, int, int] = (0, 0, 0, 255)

    def draw_color_palette(self) -> None:
        """
            Description:
        Render all color swatches onto the palette image. Iterates over
        each shade row and each color column, drawing a filled rectangle
        for every swatch
        """

        # Start below the top border
        start_row: int = 2

        for nuance in range(4):

            # Start to the right of the left border
            start_col: int = 2

            for color in self.colors:

                self.draw_color(
                    start_col,
                    start_row,
                    color.nuances[nuance]
                )

                start_col += self.column_width

            start_row += self.row_height

    def draw_color(self, x: int, y: int, color: tuple) -> None:
        """
            Description:
        Fill a single color swatch rectangle on the palette image by
        setting every pixel within the cell to the given color

            Parameters:
        x -> the left pixel coordinate of the swatch
        y -> the top pixel coordinate of the swatch
        color -> the RGBA tuple to fill the swatch with
        """

        for row in range(y, y + self.row_height):

            for col in range(x, x + self.column_width):

                img_put_px(
                    col,
                    row,
                    self.buf,
                    self.sz_line,
                    self.bpp,
                    color
                )

    def get_color_clicked(self, x: int, y: int) -> None:
        """
            Description:
        Determine which color swatch was clicked based on the given window
        coordinates and store it in color_picked. Does nothing if the click
        falls outside the drawable area inside the palette border

            Parameters:
        x -> the x coordinate of the click in the window
        y -> the y coordinate of the click in the window
        """

        # Reject clicks outside the inner drawable area of the palette
        if not (self.win_pos[0] + 2 <= x < self.win_pos[0] + self.width - 2):
            return None

        if not (self.win_pos[1] + 2 <= y < self.win_pos[1] + self.height - 2):
            return None

        # Start below the top border
        start_row: int = self.win_pos[1] + 2

        for nuance in range(4):

            start_col: int = self.win_pos[0] + 2
            end_row: int = start_row + self.row_height

            for color in range(len(self.colors)):

                end_col: int = start_col + self.column_width

                # Check if the click falls within this swatch's bounds
                if start_col <= x < end_col and start_row <= y < end_row:

                    self.color_picked = self.colors[color].nuances[nuance]
                    return None

                start_col += self.column_width

            start_row += self.row_height

    def display_img(self) -> None:
        """
            Description:
        Render the palette image onto the window at its configured position
        """

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.win_pos
        )

    def clean_img(self) -> None:
        """
            Description:
        Clear the palette image buffer and destroy the MLX image to free
        the associated memory. Should be called before closing the window
        """

        clear_img(self.buf, self.height, self.sz_line)

        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)


# The ordered sequence of color families used to cycle through in rainbow mode
RAINBOW_PALETTE: list[Colors] = [
    Colors.RED,
    Colors.ORANGE,
    Colors.YELLOW,
    Colors.GREEN_1,
    Colors.GREEN_2,
    Colors.BLUE_1,
    Colors.BLUE_2,
    Colors.VIOLET
]
