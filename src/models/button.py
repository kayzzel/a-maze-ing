import time
from ..utils import clear_img, img_put_px, draw_borders

# the width and depth of the button border

BORDER_WIDTH: int = 2
BORDER_DEPTH: int = 8


class Button:

    """

    ---- initializing the button ----

    [parameters needed]

     => name: the name of the button (displayed in the center)
     => button_sz: the width and height of the button
     => button_pos: the base position of the button in the button image
     => color: the color for the border
     => img_sz: the size of the button image
     => button_img_pos: the position of the button image in the window
     => mlx_data: the mlx object, the mlx pointer and the mlx window

    [attributes of the class]

     => end_pos: the end position of the button in the image
            (needed to know the button area when clicking with the mouse)
     => name_pos: the position of the button name in the window
     => not_clicked:
            a dictionary containing
            the image where no buttons are press
            and its data
     => clicked:
            a dictionary containing
            the image where the button is pressed
            and its data
     => needs_refresh: indicates whether or not
            the button needs to be rendered
     => is_pressed: indicates whether or not
            the button is being pressed
            (needed for the animation)
     => press_start_time: tracks the elapsed time
            since the button was pressed
     => press_duration:
            sets the maximum time for the clicking animation to last

    """

    def __init__(
        self,
        name: str,
        button_sz: tuple[int, int],
        button_pos: tuple[int, int],
        color: tuple[int, int, int, int],
        img_sz: tuple[int, int],
        button_img_pos: tuple[int, int]
    ) -> None:

        self.name: str = name
        self.color: tuple = color
        self.width, self.height = button_sz
        self.base_pos: tuple[int, int] = button_pos
        self.end_pos: tuple[int, int] = (
            self.base_pos[0] + self.width,
            self.base_pos[1] + self.height
        )
        self.win_pos: tuple[int, int] = button_img_pos
        self.name_pos: tuple[int, int] = (
            self.win_pos[0] + self.base_pos[0] + (
                (self.width - len(name) * 10) // 2
            ),
            self.win_pos[1] + self.base_pos[1]
            + self.height // 2 - 10
        )
        self.not_clicked: dict
        self.clicked: dict
        self.img_sz: tuple[int, int] = img_sz
        self.needs_refresh: bool = False
        self.is_pressed: bool = False
        self.press_start_time: float = 0
        self.press_duration: float = 0.08

    """

    draws the button borders on the image provided
    with the correct offset

    """
    def draw(
        self,
        img_data: tuple[memoryview, int, int],
        offset: int
    ) -> None:

        s_x: int = self.base_pos[0] - offset
        s_y: int = self.base_pos[1] - offset
        e_x: int = s_x + self.width
        e_y: int = s_y + self.height

        draw_borders(
            (s_x, s_y),
            (e_x, e_y),
            BORDER_WIDTH,
            img_data,
            self.color
        )

        s_x += BORDER_WIDTH
        s_y += BORDER_WIDTH
        e_x -= BORDER_WIDTH
        e_y -= BORDER_WIDTH

        draw_borders(
            (s_x + BORDER_DEPTH, s_y + BORDER_DEPTH),
            (e_x - BORDER_DEPTH, e_y - BORDER_DEPTH),
            BORDER_WIDTH,
            img_data,
            self.color
        )

        positions: tuple[int, int, int, int] = (s_x, s_y, e_x, e_y)
        s_x, s_y, e_x, e_y = positions

        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(s_x, s_y, *img_data, self.color)
            s_x += 1
            s_y += 1

        s_x, s_y, e_x, e_y = positions

        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(e_x, s_y, *img_data, self.color)
            e_x -= 1
            s_y += 1

        s_x, s_y, e_x, e_y = positions

        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(s_x, e_y, *img_data, self.color)
            s_x += 1
            e_y -= 1

        s_x, s_y, e_x, e_y = positions

        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(e_x, e_y, *img_data, self.color)
            e_x -= 1
            e_y -= 1

    """

    updates the button state and offset for the correct click display

    """

    def update(self) -> None:

        if not self.is_pressed:
            self.needs_refresh = False
            return None

        # checks if the clicking animation is over

        if time.monotonic() - self.press_start_time >= self.press_duration:

            self.is_pressed = False
            self.needs_refresh = True

    """

    clears and destroys the button's clicking image

    """

    def clean_img(self, mlx_data: tuple) -> None:

        buf, sz_line, bpp = self.clicked["img_data"]

        clear_img(buf, self.img_sz[1], sz_line)

        mlx_data[0].mlx_destroy_image(mlx_data[1], self.clicked["img"])

    """

    starts the clicking animation

    """

    def click_button(self) -> None:

        # checks if the button is already being pressed

        if self.is_pressed:
            return None

        self.is_pressed = True
        self.needs_refresh = True
        self.press_start_time = time.monotonic()


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

    button_img_sz: tuple[int, int] = (
        win_sz[0],
        win_sz[1] // 8 + 100
    )
    button_image_pos: tuple[int, int] = (
        (0, win_sz[1] - (win_sz[1] // 8 + 100))
    )

    buttons: list[Button] = []

    button_width: int = (
        win_sz[0] // len(button_names) - 100
    )
    button_height: int = win_sz[1] // 8
    horizontal_offset: int = (
        win_sz[0] - len(button_names) * button_width
    ) // (len(button_names) + 1)

    # initializing each button with the correct values

    for button_number in range(len(button_names)):

        button_pos: tuple[int, int] = (
            (
                button_width * button_number
                + horizontal_offset * (button_number + 1)
            ),
            50
        )

        buttons.append(Button(
            button_names[button_number],
            (button_width, button_height),
            button_pos,
            (255, 255, 255, 255),
            button_img_sz,
            button_image_pos
        ))

    # rendering the button image where no buttons are pressed

    none_clicked_img = mlx_data[0].mlx_new_image(
        mlx_data[1],
        *button_img_sz
    )
    buf, bpp, sz_line, _ = mlx_data[0].mlx_get_data_addr(none_clicked_img)
    clear_img(buf, button_img_sz[1], sz_line)

    for button in buttons:

        button.draw(
            (buf, sz_line, bpp),
            0
        )

    # setting the no clicked image of each button

    for button in buttons:

        button.not_clicked = {
            "img": none_clicked_img,
            "img_data": (buf, sz_line, bpp)
        }

    # rendering all the pressed button images

    for b in range(len(buttons)):

        # initializing a new image for each button

        clicked_img = mlx_data[0].mlx_new_image(
            mlx_data[1],
            *button_img_sz
        )
        buf, bpp, sz_line, _ = mlx_data[0].mlx_get_data_addr(
            clicked_img
        )
        clear_img(buf, button_img_sz[1], sz_line)

        for button_nb in range(len(buttons)):

            # setting the offset to draw the button
            # at the correct position on the image

            offset: int = 0

            if button_nb == b:
                offset = 2

            buttons[button_nb].draw(
                (buf, sz_line, bpp),
                offset
            )

        # setting the clicked button image
        # to the corresponding button

        buttons[b].clicked = {
            "img": clicked_img,
            "img_data": (buf, sz_line, bpp)
        }

    return buttons
