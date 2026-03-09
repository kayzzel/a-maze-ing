from enum import Enum
from ..utils import img_put_px, clear_img, draw_borders


class Color:

    def __init__(
        self,
        colors: list[tuple[int, int, int, int]]
    ) -> None:

        self.dark: tuple = colors[0]
        self.medium: tuple = colors[1]
        self.bright: tuple = colors[2]
        self.light: tuple = colors[3]
        self.nuances: list[tuple] = colors


class Colors(list, Enum):

    RED = [
        (79, 20, 14, 255),
        (115, 29, 20, 255),
        (176, 50, 33, 255),
        (212, 88, 76, 255)
    ]
    ORANGE = [
        (102, 49, 16, 255),
        (138, 64, 22, 255),
        (181, 81, 24, 255),
        (227, 126, 70, 255)
    ]
    YELLOW = [
        (94, 74, 10, 255),
        (130, 104, 18, 255),
        (171, 136, 21, 255),
        (214, 181, 71, 255)
    ]
    GREEN_1 = [
        (38, 56, 10, 255),
        (68, 99, 19, 255),
        (104, 145, 28, 255),
        (163, 201, 85, 255)
    ]
    GREEN_2 = [
        (12, 69, 21, 255),
        (20, 122, 35, 255),
        (28, 173, 51, 255),
        (74, 224, 98, 255)
    ],
    BLUE_1 = [
        (15, 84, 78, 255),
        (23, 128, 119, 255),
        (33, 173, 163, 255),
        (76, 224, 213, 255)
    ]
    BLUE_2 = [
        (15, 51, 84, 255),
        (25, 80, 128, 255),
        (38, 114, 181, 255),
        (91, 166, 227, 255)
    ]
    VIOLET = [
        (40, 12, 74, 255),
        (73, 21, 122, 255),
        (105, 31, 173, 255),
        (174, 128, 217, 255)
    ]
    PINK = [
        (99, 21, 56, 255),
        (148, 33, 83, 255),
        (184, 50, 108, 255),
        (222, 100, 152, 255)
    ]
    GREY = [
        (0, 0, 0, 255),
        (61, 58, 58, 255),
        (138, 129, 129, 255),
        (255, 255, 255, 255)
    ]


class ColorPalette:

    def __init__(self, mlx_data: tuple, win_sz: tuple) -> None:

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

        self.width: int = win_sz[0] // 2 + 4
        self.height: int = win_sz[1] // 5 + 4

        self.win_pos: tuple[int, int] = (
            200,
            win_sz[1] - self.height - 50
        )
        self.end_pos: tuple[int, int] = (
            self.win_pos[0] + self.width,
            self.win_pos[1] + self.height
        )

        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )

        self.buf, self.bpp, self.sz_line, _ = self.mlx.mlx_get_data_addr(
            self.img
        )

        clear_img(self.buf, self.height, self.sz_line)

        draw_borders(
            (0, 0),
            (self.width, self.height),
            2,
            (self.buf, self.sz_line, self.bpp),
            (255, 255, 255, 255)
        )

        self.column_width: int = (self.width - 4) // len(self.colors)
        self.row_height: int = (self.height - 4) // len(self.colors[0].nuances)

        self.draw_color_palette()

        self.color_picked: tuple[int, int, int, int] = (0, 0, 0, 255)

    def draw_color_palette(self) -> None:

        start_row: int = 2

        for nuance in range(4):

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

        if not (self.win_pos[0] + 2 <= x < self.win_pos[0] + self.width - 2):
            return None

        if not (self.win_pos[1] + 2 <= y < self.win_pos[1] + self.height - 2):
            return None

        start_row: int = self.win_pos[1] + 2

        for nuance in range(4):

            start_col: int = self.win_pos[0] + 2
            end_row: int = start_row + self.row_height

            for color in range(len(self.colors)):

                end_col: int = start_col + self.column_width

                if start_col <= x < end_col and start_row <= y < end_row:

                    self.color_picked = self.colors[color].nuances[nuance]
                    return None

                start_col += self.column_width

            start_row += self.row_height

    def display_img(self) -> None:

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.win_pos
        )

    def clean_img(self) -> None:

        clear_img(self.buf, self.height, self.sz_line)

        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)
