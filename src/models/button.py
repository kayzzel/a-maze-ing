import time
from ..utils import clear_img, img_put_px


BORDER_WIDTH: int = 2


class Button:

    def __init__(
        self,
        name: str,
        win_sz: tuple[int, int],
        nb_button: int,
        color: tuple[int, int, int, int],
        mlx_data: tuple
    ) -> None:

        self.name: str = name
        self.number: int = nb_button
        self.color: tuple = color
        self.depth: int = 8
        self.width: int = win_sz[0] // 5 + 25
        self.height: int = win_sz[1] // 8
        self.win_sz: tuple[int, int] = win_sz
        self.base_pos: tuple[int, int] = (
            (25 + self.width) * self.number + 15,
            self.win_sz[1] - (self.height + 50)
        )
        self.offset: int = 0
        self.end_pos: tuple[int, int] = (
            self.base_pos[0] + self.width,
            self.base_pos[1] + self.height
        )
        self.name_pos: tuple[int, int] = (
            self.base_pos[0] + (
                (self.width - len(name) * 8) // 3
            ),
            self.base_pos[1] + self.height // 2 - 10
        )
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )
        self.buf, self.bpp, self.sz_line, *oth = (
            self.mlx.mlx_get_data_addr(self.img)
        )
        self.is_pressed: bool = False
        self.press_start_time: float = 0
        self.press_duration: float = 0.08

    def draw(self) -> None:

        clear_img(self.buf)

        for row in range(self.height):

            for col in range(self.width):

                if self.is_outline(col, row):
                    img_put_px(
                        col,
                        row,
                        self.buf,
                        self.sz_line,
                        self.bpp,
                        self.color
                    )

    def update(self) -> None:

        if not self.is_pressed:
            return None

        if time.time() - self.press_start_time < self.press_duration:
            self.offset = 2

        else:
            self.offset = 0
            self.is_pressed = False

        self.draw()

    def is_outline(self, x: int, y: int) -> bool:

        posx: list[int] = [
            x for x in range(
                self.width - BORDER_WIDTH - self.depth,
                self.width - BORDER_WIDTH
            )
        ]
        posy: list[int] = [
            y for y in range(
                self.height - BORDER_WIDTH - self.depth,
                self.height - BORDER_WIDTH
            )
        ]

        for pos in range(
            BORDER_WIDTH, BORDER_WIDTH + self.depth
        ):
            if (x, y) == (pos, pos):
                return True

        for pos in range(len(posx)):
            if (x, y) == (posx[-(pos + 1)], pos + BORDER_WIDTH):
                return True

            if (x, y) == (pos + BORDER_WIDTH, posy[-(pos + 1)]):
                return True

            if (x, y) == (posx[pos], posy[pos]):
                return True

        for pos in [0, BORDER_WIDTH + self.depth]:

            if (
                pos <= x < pos + BORDER_WIDTH
                or self.width - pos - BORDER_WIDTH
                <= x < self.width - pos
            ) and pos <= y < self.height - pos:
                return True

            if (
                pos <= y < pos + BORDER_WIDTH
                or self.height - pos - BORDER_WIDTH
                <= y < self.height - pos
            ) and pos <= x < self.width - pos:
                return True

        return False

    def click_button(self) -> None:

        if self.is_pressed:
            return None

        self.is_pressed = True
        self.press_start_time = time.time()

    def clean_img(self) -> None:

        clear_img(self.buf)
        self.mlx.mlx_destroy_image(
            self.mlx_ptr,
            self.img
        )


def generate_buttons(mlx_data: tuple, win_sz: tuple[int, int]) -> list[Button]:

    button_names: list[str] = [
        "Generate new maze",
        "Toggle path on/off",
        "Change colors",
        "Exit window"
    ]

    buttons: list[Button] = []

    for button_number in range(len(button_names)):
        buttons.append(Button(
            button_names[button_number],
            win_sz,
            button_number,
            (255, 255, 255, 255),
            mlx_data
        ))

    return buttons
