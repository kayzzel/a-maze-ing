import time
from ..utils import clear_img, img_put_px

# the width and depth of the button border

BORDER_WIDTH: int = 2
BORDER_DEPTH: int = 8


class Button:

    """

    ---- initializing the button ----

    [parameters needed]

     => name: the name of the button (displayed in the center)
     => button_sz: the width and height of the button
     => button_pos: the base position of the button in the window
     => color: the color for the border
     => mlx_data: the mlx object, the mlx pointer and the mlx window

    [attributes of the class]

     => end_pos: the end position of the button
            (needed to know the button area when clicking with the mouse)
     => offset: the offset added to base_pos for the click animation
     => name_pos: the position of the button name in the window
     => img: the button image
     => is_pressed: indicates whether or not the button is being pressed
            (needed for the animation)
     => press_start_time: tracks the elapsed time since the button was pressed
     => press_duration:
            sets the maximum time for the clicking animation to last

    """

    def __init__(
        self,
        name: str,
        button_sz: tuple[int, int],
        button_pos: tuple[int, int],
        color: tuple[int, int, int, int],
        mlx_data: tuple
    ) -> None:

        self.name: str = name
        self.color: tuple = color
        self.width, self.height = button_sz
        self.base_pos: tuple[int, int] = button_pos
        self.end_pos: tuple[int, int] = (
            self.base_pos[0] + self.width,
            self.base_pos[1] + self.height
        )
        self.offset: int = 0
        self.name_pos: tuple[int, int] = (
            self.base_pos[0] + (
                (self.width - len(name) * 10) // 2
            ),
            self.base_pos[1] + self.height // 2 - 10
        )
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            self.width,
            self.height
        )
        self.buf, self.bpp, self.sz_line, _ = (
            self.mlx.mlx_get_data_addr(self.img)
        )
        clear_img(self.buf, self.height, self.sz_line)
        self.is_pressed: bool = False
        self.press_start_time: float = 0
        self.press_duration: float = 0.08
        self.needs_refresh: bool = True
        self.posx: list[int] = [
            x for x in range(
                self.width - BORDER_WIDTH - BORDER_DEPTH,
                self.width - BORDER_WIDTH
            )
        ]
        self.posy: list[int] = [
            y for y in range(
                self.height - BORDER_WIDTH - BORDER_DEPTH,
                self.height - BORDER_WIDTH
            )
        ]

    """

    draws the button border on the image

    """
    def draw(self) -> None:

        # clear_img(self.buf, self.height, self.sz_line)

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

    """

    updates the button state and offset for the correct click display

    """

    def update(self) -> None:

        if not self.is_pressed:
            self.needs_refresh = False
            return
            # checks if the clicking animation is over

        if time.monotonic() - self.press_start_time >= self.press_duration:

            self.offset = 0
            self.is_pressed = False
            self.needs_refresh = True

        if self.needs_refresh:
            self.draw()

    """

    verifies if the current pixel is part of the border and needs to be drawn

    """

    def is_outline(self, col: int, row: int) -> bool:

        for pos in range(
            BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH
        ):
            if (col, row) == (pos, pos):
                return True

        for pos in range(len(self.posx)):
            if (col, row) == (self.posx[-(pos + 1)], pos + BORDER_WIDTH):
                return True

            if (col, row) == (pos + BORDER_WIDTH, self.posy[-(pos + 1)]):
                return True

            if (col, row) == (self.posx[pos], self.posy[pos]):
                return True

        for pos in [0, BORDER_WIDTH + BORDER_DEPTH]:

            if (
                pos <= col < pos + BORDER_WIDTH
                or self.width - pos - BORDER_WIDTH
                <= col < self.width - pos
            ) and pos <= row < self.height - pos:
                return True

            if (
                pos <= row < pos + BORDER_WIDTH
                or self.height - pos - BORDER_WIDTH
                <= row < self.height - pos
            ) and pos <= col < self.width - pos:
                return True

        return False

    """

    starts the clicking animation

    """

    def click_button(self) -> None:

        # checks if the button is already being pressed

        if self.is_pressed:
            return None

        self.is_pressed = True
        self.needs_refresh = True
        self.offset = 2
        self.press_start_time = time.monotonic()

    """

    clears the button image and destroys it

    """

    def clean_img(self) -> None:

        clear_img(self.buf, self.height, self.sz_line)

        self.mlx.mlx_destroy_image(
            self.mlx_ptr,
            self.img
        )


"""

generates all the buttons needed for the display

"""


def generate_buttons(mlx_data: tuple, win_sz: tuple[int, int]) -> list[Button]:

    button_names: list[str] = [
        "Generate new maze",
        "Toggle path on/off",
        "Change colors",
        "Rainbow mode",
        "Exit window"
    ]

    buttons: list[Button] = []

    button_width: int = (
        win_sz[0] // len(button_names) - 100
    )
    button_height: int = win_sz[1] // 8
    horizontal_offset: int = (
        win_sz[0] -
        (button_width * len(button_names))
    ) // (len(button_names) + 1)

    for button_number in range(len(button_names)):

        button_pos: tuple[int, int] = (
            (
                button_width * button_number
                + horizontal_offset * (button_number + 1)
            ),
            win_sz[1] - (button_height + 50)
        )

        buttons.append(Button(
            button_names[button_number],
            (button_width, button_height),
            button_pos,
            (255, 255, 255, 255),
            mlx_data
        ))

    # uncomment the following and comment those up
    # if you want the buttons to be displayed on two lines

    """
    lines: list[list[str]] = [
        button_names[:len(button_names) // 2 + 1],
        button_names[len(button_names) // 2 + 1:]
    ]

    for line in range(len(lines)):

        horizontal_offset: int = (
            win_sz[0] -
            (button_width * len(lines[line]))
        ) // (len(lines[line]) + 1)

        vertical_offset: int = len(lines) - line

        for button_number in range(len(lines[line])):

            button_pos: tuple[int, int] = (
                (
                    button_width * button_number
                    + horizontal_offset * (button_number + 1)
                ),
                win_sz[1] - vertical_offset * (button_height + 35)
            )

            buttons.append(Button(
                lines[line][button_number],
                (button_width, button_height),
                button_pos,
                (255, 255, 255, 255),
                mlx_data
            ))
    """

    return buttons
