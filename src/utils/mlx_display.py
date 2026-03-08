from typing import Any


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

    # checks if the button image needs to be changed

    if not button_menu.needs_refresh():

        mlx.mlx_put_image_to_window(
            mlx_ptr,
            mlx_win,
            maze.img,
            *maze.maze_pos
        )

        return None

    mlx.mlx_clear_window(mlx_ptr, mlx_win)

    # puts the maze image on the window

    mlx.mlx_put_image_to_window(
        mlx_ptr,
        mlx_win,
        maze.img,
        *maze.maze_pos
    )

    button_menu.display_button_menu()


"""

returns the entire color palette for the maze
if you want to add colors, do it directly here

"""


def get_color_palette() -> list[list[tuple[int, int, int, int]]]:

    return [
        [
            (0, 0, 255, 255),
            (255, 255, 255, 255),
            (255, 0, 0, 255)
        ],
        [
            (0, 255, 0, 255),
            (255, 255, 255, 255),
            (0, 0, 255, 255)
        ],
        [
            (255, 0, 0, 255),
            (255, 255, 255, 255),
            (0, 255, 0, 255)
        ]
    ]


"""

returns a rainbow color palette

"""


def get_rainbow_palette() -> list[list[tuple[int, int, int, int]]]:

    return [
        [
            (99, 31, 17, 255),
            (219, 110, 88, 255),
            (173, 39, 12, 255)
        ],
        [
            (120, 63, 16, 255),
            (212, 146, 93, 255),
            (207, 108, 27, 255)
        ],
        [
            (150, 132, 26, 255),
            (222, 204, 100, 255),
            (209, 184, 44, 255)
        ],
        [
            (67, 122, 18, 255),
            (166, 217, 121, 255),
            (106, 194, 29, 255)
        ],
        [
            (63, 140, 29, 255),
            (139, 217, 106, 255),
            (87, 186, 45, 255)
        ],
        [
            (27, 139, 143, 255),
            (120, 218, 222, 255),
            (47, 209, 214, 255)
        ],
        [
            (25, 29, 138, 255),
            (101, 127, 219, 255),
            (33, 68, 194, 255)
        ],
        [
            (63, 19, 112, 255),
            (176, 132, 227, 255),
            (102, 26, 189, 255)
        ]
    ]
