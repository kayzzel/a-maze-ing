from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models.button_menu import ButtonMenu
    from ..models.maze_display import MazeDisplay
from .letters import LETTERS, ALLOWED_LETTERS


def img_put_px(
    x: int,
    y: int,
    buf: memoryview,
    sz_line: int,
    bpp: int,
    color: tuple[int, int, int, int]
) -> None:
    """
        Description:
    Set the color of a single pixel in an MLX image buffer at the given
    coordinates by writing the RGBA components to the correct memory offset

        Parameters:
    x -> the x coordinate of the pixel in the image
    y -> the y coordinate of the pixel in the image
    buf -> the memoryview of the image buffer
    sz_line -> the number of bytes per row in the buffer
    bpp -> the number of bits per pixel
    color -> the RGBA color tuple to write as (r, g, b, a)
    """

    r: int
    g: int
    b: int
    a: int
    b, g, r, a = color

    # Compute the byte offset of this pixel in the buffer
    offset: int = y * sz_line + x * (bpp // 8)

    buf[offset + 0] = r
    buf[offset + 1] = g
    buf[offset + 2] = b
    buf[offset + 3] = a


def draw_borders(
    start_pos: tuple[int, int],
    end_pos: tuple[int, int],
    border_width: int,
    img_data: tuple[memoryview, int, int],
    color: tuple[int, int, int, int]
) -> None:
    """
        Description:
    Draw a filled rectangular border of the given thickness onto an MLX
    image buffer. Each of the four sides is drawn independently

        Parameters:
    start_pos -> the (x, y) top-left corner of the bordered area
    end_pos -> the (x, y) bottom-right corner of the bordered area
    border_width -> the thickness of the border in pixels
    img_data -> the image buffer as (buf, sz_line, bpp)
    color -> the RGBA color tuple to use for the border
    """

    start_x: int
    start_y: int
    end_x: int
    end_y: int
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # Top border
    for y in range(start_y, start_y + border_width):
        for x in range(start_x, end_x):
            img_put_px(x, y, *img_data, color)

    # Bottom border
    for y in range(end_y - border_width, end_y):
        for x in range(start_x, end_x):
            img_put_px(x, y, *img_data, color)

    # Left border
    for x in range(start_x, start_x + border_width):
        for y in range(start_y, end_y):
            img_put_px(x, y, *img_data, color)

    # Right border
    for x in range(end_x - border_width, end_x):
        for y in range(start_y, end_y):
            img_put_px(x, y, *img_data, color)


def render(
    maze: "MazeDisplay",
    button_menu: "ButtonMenu",
    mlx_data: tuple
) -> None:
    """
        Description:
    Render the current frame by displaying the button menu and the maze
    image onto the window

        Parameters:
    maze -> the MazeDisplay instance to render
    button_menu -> the ButtonMenu instance to render
    mlx_data -> a tuple containing (mlx, mlx_ptr, mlx_win) for the MLX instance
    """

    mlx, mlx_ptr, mlx_win = mlx_data
    button_menu.display_button_menu()
    maze.display_on_window()


def put_str_to_img(
        string: str,
        buf: memoryview,
        str_coord: tuple[int, int],
        size_line: int,
        bpp: int,
        color: tuple[int, int, int, int],
        ) -> None:
    """
        Description:
    Render a string of characters onto an MLX image buffer using a
    bitmap font. Each character is drawn from the LETTERS lookup table
    at a horizontally offset position. Only characters present in
    ALLOWED_LETTERS are accepted

        Parameters:
    string -> the string to render, must contain only allowed characters
    buf -> the memoryview of the image buffer to draw onto
    str_coord -> the (x, y) position of the first character in the image
    size_line -> the number of bytes per row in the buffer
    bpp -> the number of bits per pixel
    color -> the RGBA color tuple to use for the text
    """

    # Reject strings containing characters outside the supported set
    if not all(letter in ALLOWED_LETTERS for letter in string):
        raise ValueError(
                "the str must be composed only of letters and spaces"
                f"entry: {string}"
                )

    for index in range(len(string)):

        letter: list[list[int]] = LETTERS[string[index].lower()]

        # Advance the x position by the character width plus a 2-pixel gap
        x_offset = str_coord[0] + (len(letter[0]) + 2) * index
        y_offset = str_coord[1]

        for y in range(len(letter)):

            for x in range(len(letter[0])):

                # Skip pixels where the bitmap value is 0 (empty)
                if letter[y][x] == 0:
                    continue

                img_put_px(
                        x + x_offset, y + y_offset, buf, size_line, bpp, color
                        )
