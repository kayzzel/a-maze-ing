from .button import Button
from ..utils.mlx_display import put_str_to_img
from ..utils.cleanup import clear_img


class Input:
    """
        Description:
    A text input widget that captures keystrokes for a settings field
    and renders the prompt and current input string onto an MLX image
    centered in the window

        Parameters:
    win_sz -> the size of the window as (width, height)
    mlx_data -> a tuple containing (mlx, mlx_ptr, mlx_win) for the MLX instance

        Attributes:
    taking_input -> True while the widget is actively collecting input
    cur_setting -> the Button corresponding to the setting being edited,
                   or None if no setting is active
    user_input -> the list of characters or digits entered so far
    input_title -> the prompt string displayed above the input field
    win_sz -> the window size
    mlx, mlx_ptr, mlx_win -> the MLX rendering context
    img_sz -> the size of the input image as (width, height)
    img -> the MLX image used to render the input widget
    img_pos -> the (x, y) position of the image in the window
    buf, bpp, sz_line -> the raw image buffer and its parameters
    """

    def __init__(
        self,
        win_sz: tuple[int, int],
        mlx_data: tuple
    ) -> None:

        self.taking_input: bool = False
        self.cur_setting: Button | None = None
        self.user_input: list = []
        self.input_title: str = ""
        self.win_sz: tuple[int, int] = win_sz
        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.initialize_img()

    def reset(self) -> None:
        """
            Description:
        Reset the input widget to its idle state by clearing the active
        setting, the collected input, and the taking_input flag
        """

        self.taking_input = False
        self.cur_setting = None
        self.user_input = []

    def initialize_img(self) -> None:
        """
            Description:
        Allocate the MLX image used to render the input widget and
        compute its size and centered position within the window.
        Clears the image buffer on creation
        """

        # Size the image to the full window width and one eighth of its height
        self.img_sz: tuple[int, int] = (
            self.win_sz[0],
            self.win_sz[1] // 8
        )

        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            *self.img_sz
        )

        # Center the image vertically in the window
        self.img_pos: tuple[int, int] = (
            0,
            (self.win_sz[1] - self.img_sz[1]) // 2
        )

        self.buf, self.bpp, self.sz_line, _ = self.mlx.mlx_get_data_addr(
            self.img
        )

        clear_img(self.buf, self.img_sz[1], self.sz_line)

    def update(self) -> None:
        """
            Description:
        Redraw the input widget image with the current prompt title and
        the user's input string. The title is centered horizontally near
        the top and the input string is centered near the bottom of the
        image. Does nothing if input is not currently being collected
        """

        if not (
            self.taking_input
            and self.cur_setting
        ):
            return None

        # Clear the window and the image buffer before redrawing
        self.mlx.mlx_clear_window(self.mlx_ptr, self.mlx_win)
        clear_img(self.buf, self.img_sz[1], self.sz_line)

        # Build and center the prompt title at the top of the image
        self.input_title = (
            f"Enter value for {self.cur_setting.name} "
            "parameter:"
        )
        self.title_pos: tuple[int, int] = (
            (self.img_sz[0] - len(self.input_title) * 12) // 2,
            0
        )

        put_str_to_img(
            self.input_title,
            self.buf,
            self.title_pos,
            self.sz_line,
            self.bpp,
            (255, 255, 255, 255)
        )

        # Draw the current input string centered near the bottom of the image
        if self.user_input:
            self.input_string: str = "".join([
                str(val) for val in self.user_input
            ])
            self.input_pos: tuple[int, int] = (
                (self.img_sz[0] - len(self.input_string) * 12) // 2,
                self.img_sz[1] - 25
            )
            put_str_to_img(
                self.input_string,
                self.buf,
                self.input_pos,
                self.sz_line,
                self.bpp,
                (255, 255, 255, 255)
            )

    def display_img_on_window(self) -> None:
        """
            Description:
        Render the input widget image onto the window at its configured
        position. Does nothing if input is not currently being collected
        """

        if not self.taking_input:
            return None

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.img_pos
        )

    def clean_img(self) -> None:
        """
            Description:
        Clear the image buffer and destroy the MLX image to free the
        associated memory. Should be called before closing the window
        """

        clear_img(self.buf, self.img_sz[1], self.sz_line)

        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)
