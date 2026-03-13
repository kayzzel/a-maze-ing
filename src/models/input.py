from .button import Button
from ..utils.mlx_display import put_str_to_img
from ..utils.cleanup import clear_img


class Input:

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

        self.taking_input = False
        self.cur_setting = None
        self.user_input = []

    def initialize_img(self) -> None:

        self.img_sz: tuple[int, int] = (
            self.win_sz[0],
            self.win_sz[1] // 8
        )
        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            *self.img_sz
        )
        self.img_pos: tuple[int, int] = (
            0,
            (self.win_sz[1] - self.img_sz[1]) // 2
        )
        self.buf, self.bpp, self.sz_line, _ = self.mlx.mlx_get_data_addr(
            self.img
        )

        clear_img(self.buf, self.img_sz[1], self.sz_line)

    def update(self) -> None:

        if not (
            self.taking_input
            and self.cur_setting
        ):
            return None

        self.mlx.mlx_clear_window(self.mlx_ptr, self.mlx_win)
        clear_img(self.buf, self.img_sz[1], self.sz_line)

        self.input_title = (
            f"Enter value for {self.cur_setting.name.split(' :', 1)[0]} "
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

        if self.user_input:

            self.input_string: str = "".join([
                str(val) for val in self.user_input
            ])
            self.input_pos: tuple[int, int] = (
                (self.img_sz[0] - len(self.input_string) * 12) // 2,
                self.img_sz[1] - 30
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

        if not self.taking_input:
            return None

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.img_pos
        )

    def clean_img(self) -> None:

        clear_img(self.buf, self.img_sz[1], self.sz_line)

        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)
