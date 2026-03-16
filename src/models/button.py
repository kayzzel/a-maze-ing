import time
from ..utils.cleanup import clear_img
from ..utils.mlx_display import img_put_px, draw_borders, put_str_to_img


# Width and depth used to draw the 3D-like button borders
BORDER_WIDTH: int = 2
BORDER_DEPTH: int = 8


class Button:

    """
        Description:
    Represent a clickable button displayed inside an image.
    The button contains two visual states (pressed / not pressed)
    and handles its own click animation.

        Parameters:
    name -> text displayed at the center of the button
    button_sz -> width and height of the button
    button_pos -> base position of the button inside the button image
    color -> color used to draw the button borders
    img_sz -> size of the button image
    button_img_pos -> position of the button image inside the window

        Attributes:
    end_pos -> end position of the button inside the image
               (used to detect mouse clicks inside the button area)

    name_pos -> position where the button name is drawn

    not_clicked -> dictionary containing the image and data
                   of the button when it is not pressed

    clicked -> dictionary containing the image and data
               of the button when it is pressed

    needs_refresh -> indicates whether the button needs to be redrawn

    is_pressed -> indicates whether the button is currently pressed
                  (used for the click animation)

    press_start_time -> time when the button was pressed

    press_duration -> duration of the click animation
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

        # Button display name
        self.name: str = name

        # Color used for the borders
        self.color: tuple = color

        # Button size
        self.width, self.height = button_sz

        # Base position inside the button image
        self.base_pos: tuple[int, int] = button_pos

        # End position inside the image
        self.end_pos: tuple[int, int] = (
            self.base_pos[0] + self.width,
            self.base_pos[1] + self.height
        )

        # Position of the button image inside the window
        self.img_pos: tuple[int, int] = button_img_pos

        # Button start position relative to the window
        self.start_win_pos: tuple[int, int] = (
            self.img_pos[0] + self.base_pos[0],
            self.img_pos[1] + self.base_pos[1],
        )

        # Button end position relative to the window
        self.end_win_pos: tuple[int, int] = (
            self.img_pos[0] + self.end_pos[0],
            self.img_pos[1] + self.end_pos[1]
        )

        # Compute the position where the button name will be drawn
        # (rough horizontal centering based on character width)
        self.name_pos: tuple[int, int] = (
            self.base_pos[0] + (
                (self.width - len(name) * 12) // 2
            ),
            self.base_pos[1]
            + self.height // 2 - 10
        )

        # Images representing the button states
        self.not_clicked: dict
        self.clicked: dict

        # Size of the button image
        self.img_sz: tuple[int, int] = img_sz

        # Rendering flags
        self.needs_refresh: bool = False
        self.is_pressed: bool = False

        # Animation timing
        self.press_start_time: float = 0
        self.press_duration: float = 0.08

    def draw(
        self,
        img_data: tuple[memoryview, int, int],
        offset: int
    ) -> None:
        """
            Description:
        Draw the button borders and text on the given image.

        The offset is used to create the pressed animation
        by slightly shifting the drawing position.

            Parameters:
        img_data -> information about the image to draw on
                    (pixel buffer, size_line, bits_per_pixel)

        offset -> number of pixels used to offset the button
                  when simulating the pressed state
        """

        # Compute the start and end coordinates with the offset applied
        s_x: int = self.base_pos[0] - offset
        s_y: int = self.base_pos[1] - offset
        e_x: int = s_x + self.width
        e_y: int = s_y + self.height

        # Draw the outer border of the button
        draw_borders(
            (s_x, s_y),
            (e_x, e_y),
            BORDER_WIDTH,
            img_data,
            self.color
        )

        # Adjust the borders inward to draw the inner border
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

        # Save the border positions for reuse
        positions: tuple[int, int, int, int] = (s_x, s_y, e_x, e_y)
        s_x, s_y, e_x, e_y = positions

        # Draw the diagonal corners (top-left)
        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(s_x, s_y, *img_data, self.color)
            s_x += 1
            s_y += 1

        s_x, s_y, e_x, e_y = positions

        # Draw the diagonal corners (top-right)
        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(e_x, s_y, *img_data, self.color)
            e_x -= 1
            s_y += 1

        s_x, s_y, e_x, e_y = positions

        # Draw the diagonal corners (bottom-left)
        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(s_x, e_y, *img_data, self.color)
            s_x += 1
            e_y -= 1

        s_x, s_y, e_x, e_y = positions

        # Draw the diagonal corners (bottom-right)
        for _ in range(BORDER_WIDTH, BORDER_WIDTH + BORDER_DEPTH):

            img_put_px(e_x, e_y, *img_data, self.color)
            e_x -= 1
            e_y -= 1

        # Draw the button label
        put_str_to_img(
            self.name,
            img_data[0],
            (
                self.name_pos[0] - offset,
                self.name_pos[1] - offset
            ),
            img_data[1],
            img_data[2],
            (255, 255, 255, 255)
        )

    def update(self) -> None:
        """
            Description:
        Update the button state and check whether the
        clicking animation has finished.
        """

        # If the button is not pressed there is nothing to update
        if not self.is_pressed:
            self.needs_refresh = False
            return None

        # Check if the clicking animation duration has elapsed
        if time.monotonic() - self.press_start_time >= self.press_duration:

            # Stop the pressed state
            self.is_pressed = False

            # Request a redraw to update the button state
            self.needs_refresh = True

    def clean_img(self, mlx_data: tuple) -> None:
        """
            Description:
        Clear and destroy the image used for the
        pressed button state.
        """

        # Get the image buffer information
        buf, sz_line, bpp = self.clicked["img_data"]

        # Clear the image pixels
        clear_img(buf, self.img_sz[1], sz_line)

        # Destroy the image in the MLX context
        mlx_data[0].mlx_destroy_image(mlx_data[1], self.clicked["img"])

    def click_button(self) -> None:
        """
            Description:
        Start the button clicking animation.
        """

        # If the button is already being pressed
        # ignore the new click
        if self.is_pressed:
            return None

        # Start the pressed state
        self.is_pressed = True
        self.needs_refresh = True

        # Save the start time of the animation
        self.press_start_time = time.monotonic()
