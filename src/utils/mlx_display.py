from typing import Any as any


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


def render(maze: any, buttons: list, mlx_data: tuple) -> None:

    mlx, mlx_ptr, mlx_win = mlx_data

    mlx.mlx_clear_window(mlx_ptr, mlx_win)

    # puts the maze image on the window

    mlx.mlx_put_image_to_window(
        mlx_ptr,
        mlx_win,
        maze.img,
        *maze.maze_pos
    )

    # puts the button image + button title on the window for each button

    for button in buttons:

        mlx.mlx_put_image_to_window(
            mlx_ptr,
            mlx_win,
            button.img,
            button.base_pos[0] - button.offset,
            button.base_pos[1] - button.offset
        )

        mlx.mlx_string_put(
            mlx_ptr,
            mlx_win,
            button.name_pos[0] - button.offset,
            button.name_pos[1] - button.offset,
            0xFFFFFF,
            button.name
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
