from typing import Any
from .letters import LETTERS, ALLOWED_LETTERS


"""

changes the pixel of an image at the given coordinates

"""


def img_put_px(
    x: int,
    y: int,
    buf: memoryview,
    sz_line: int,
    bpp: int,
    color: tuple[int, int, int, int]
) -> None:

    r: int
    g: int
    b: int
    a: int

    b, g, r, a = color

    # calculates the buffer offset in the memory

    offset: int = y * sz_line + x * (bpp // 8)

    buf[offset + 0] = r
    buf[offset + 1] = g
    buf[offset + 2] = b
    buf[offset + 3] = a


"""

draws the borders of a button using the coordinates provided

"""


def draw_borders(
    start_pos: tuple[int, int],
    end_pos: tuple[int, int],
    border_width: int,
    img_data: tuple[memoryview, int, int],
    color: tuple[int, int, int, int]
) -> None:

    start_x: int
    start_y: int
    end_x: int
    end_y: int

    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # top border
    for y in range(start_y, start_y + border_width):
        for x in range(start_x, end_x):
            img_put_px(x, y, *img_data, color)

    # bottom border
    for y in range(end_y - border_width, end_y):
        for x in range(start_x, end_x):
            img_put_px(x, y, *img_data, color)

    # left border
    for x in range(start_x, start_x + border_width):
        for y in range(start_y, end_y):
            img_put_px(x, y, *img_data, color)

    # right border
    for x in range(end_x - border_width, end_x):
        for y in range(start_y, end_y):
            img_put_px(x, y, *img_data, color)


"""

renders both the maze and the buttons

"""


def render(
    maze: Any,
    button_menu,
    mlx_data: tuple
) -> None:

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
        ):

    if not all(letter in ALLOWED_LETTERS for letter in string):
        raise ValueError(
                "the str must be composed only of letters and spaces"
                f"entry: {string}"
                )

    for index in range(len(string)):

        letter: list[list[int]] = LETTERS[string[index].lower()]

        x_offset = str_coord[0] + (len(letter[0]) + 2) * index
        y_offset = str_coord[1]

        for y in range(len(letter)):
            for x in range(len(letter[0])):
                if letter[y][x] == 0:
                    continue
                img_put_px(
                        x + x_offset, y + y_offset, buf, size_line, bpp, color
                        )
