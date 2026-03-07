from typing import Any
from .cleanup import clear_img


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

renders both the maze and the buttons

"""


def render(maze: Any, buttons: list, mlx_data: tuple) -> None:

    mlx, mlx_ptr, mlx_win = mlx_data

    button_img = buttons[0].img
    button_img_sz: tuple[int, int] = buttons[0].img_sz
    buttons_win_pos: tuple[int, int] = buttons[0].win_pos
    buf, sz_line, bpp = buttons[0].buf, buttons[0].sz_line, buttons[0].bpp

    # puts the button image + button title on the window for each button

    if any(button.needs_refresh for button in buttons):

        clear_img(buf, button_img_sz[1], sz_line)
        for button in buttons:
            button.draw()
            mlx.mlx_string_put(
                mlx_ptr,
                mlx_win,
                button.name_pos[0] - button.offset,
                button.name_pos[1] - button.offset,
                0xFFFFFF,
                button.name
            )

        mlx.mlx_put_image_to_window(
            mlx_ptr,
            mlx_win,
            button_img,
            *buttons_win_pos
        )

    # puts the maze image on the window

    mlx.mlx_put_image_to_window(
        mlx_ptr,
        mlx_win,
        maze.img,
        *maze.maze_pos
    )


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
