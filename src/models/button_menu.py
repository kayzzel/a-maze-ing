from .button import Button
from .maze_display import MazeDisplay
from .color_palette import ColorPalette
from ..utils import clear_img, clear_all, is_in
from ..services.generation_algo.rec_backtrack import rec_backtrack
from ..services.solving_algo.a_star import a_star
from enum import Enum
import random


class ColorType(str, Enum):

    WALL = "Wall Color"
    BG = "Background Color"
    PATH = "Path Color"
    ENTRY_EXIT = "Entry/Exit Color"


class ButtonMenu:

    def __init__(
        self,
        mlx_data: tuple,
        maze_display: MazeDisplay,
        win_sz: tuple[int, int]
    ) -> None:

        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.maze: MazeDisplay = maze_display
        self.win_sz: tuple[int, int] = win_sz

        self.menus: dict = {
            "main": self.generate_buttons([
                "generate new maze",
                "path menu",
                "change colors",
                "exit window"
            ]),
            "color_change": self.generate_buttons([
                "random colors",
                "custom colors",
                "rainbow mode on/off",
                "back to menu"
            ]),
            "gen_algo_choice": self.generate_buttons([
                "wilson",
                "recursive backtracking",
                "random"
            ]),
            "path_menu": self.generate_buttons([
                "a*",
                "jump point search",
                "toggle path on/off",
                "back to menu"
            ])
        }

        self.color_palette: ColorPalette = ColorPalette(
            mlx_data,
            win_sz
        )

        self.create_ok_button()

        self.cur_menu: str = "main"

        self.button_title: str = "A-Maze-Ing Menu"

        self.color_type: ColorType

        self.menus["main"][0].needs_refresh = True
        self.display_button_menu()

    def update_buttons(self) -> None:

        self.ok_button.update()

        for menu in self.menus.values():

            for button in menu:

                button.update()

    def needs_refresh(self) -> bool:

        for menu in self.menus.values():

            if any(
                button.needs_refresh
                for button in menu
            ) or self.ok_button.needs_refresh:
                return True

        return False

    def display_button_menu(self) -> None:

        if not self.needs_refresh():
            return None

        self.mlx.mlx_clear_window(self.mlx_ptr, self.mlx_win)
        self.display_button_title()

        if self.cur_menu == "color_palette":

            self.color_palette.display_img()

            img_to_display: dict = self.ok_button.not_clicked

            if self.ok_button.is_pressed:
                img_to_display = self.ok_button.clicked

            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr,
                self.mlx_win,
                img_to_display["img"],
                *self.ok_button.img_pos
            )

            return None

        menu_to_display: list[Button] = self.menus[self.cur_menu]

        img_to_display = menu_to_display[0].not_clicked

        for button in menu_to_display:

            if button.is_pressed:
                img_to_display = button.clicked

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            img_to_display["img"],
            *menu_to_display[0].img_pos
        )

    def display_button_title(self) -> None:

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.mlx_win,
            (self.win_sz[0] - (len(self.button_title) * 10)) // 2,
            self.maze.img_pos[1] + self.maze.img_height + 25,
            0xFFFFFF,
            self.button_title
        )

    def create_ok_button(self) -> None:

        self.ok_button: Button = Button(
            "ok",
            (98, 98),
            (2, 2),
            (255, 255, 255, 255),
            (100, 100),
            (
                self.win_sz[0] - (
                    (self.win_sz[0] - self.color_palette.end_pos[0] + 200)
                    // 2
                ),
                (
                    self.color_palette.win_pos[1] +
                    (self.color_palette.height - 100) // 2
                )
            )
        )
        self.render_button_images([self.ok_button])

    """

    generates all the buttons needed for the display

    """

    def generate_buttons(self, button_names: list[str]) -> list[Button]:

        button_img_sz: tuple[int, int] = (
            self.win_sz[0],
            self.win_sz[1] // 8 + 100
        )
        button_image_pos: tuple[int, int] = (
            (0, self.win_sz[1] - (self.win_sz[1] // 8 + 100))
        )

        buttons: list[Button] = []

        button_width: int = (
            self.win_sz[0] // len(button_names) - 100
        )
        button_height: int = self.win_sz[1] // 8
        horizontal_offset: int = (
            self.win_sz[0] - len(button_names) * button_width
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

        self.render_button_images(buttons)

        return buttons

    def render_button_images(self, buttons: list[Button]) -> None:

        # rendering the button image where no buttons are pressed

        none_clicked_img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            *buttons[0].img_sz
        )
        buf, bpp, sz_line, _ = self.mlx.mlx_get_data_addr(none_clicked_img)
        clear_img(buf, buttons[0].img_sz[1], sz_line)

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

            clicked_img = self.mlx.mlx_new_image(
                self.mlx_ptr,
                *buttons[0].img_sz
            )
            buf, bpp, sz_line, _ = self.mlx.mlx_get_data_addr(
                clicked_img
            )
            clear_img(buf, buttons[0].img_sz[1], sz_line)

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

    def find_button_clicked(self, x: int, y: int) -> Button | None:

        if self.cur_menu == "color_palette":

            if is_in(
                x,
                y,
                self.ok_button.start_win_pos,
                self.ok_button.end_win_pos
            ):
                return self.ok_button

            if is_in(
                x,
                y,
                self.color_palette.win_pos,
                self.color_palette.end_pos
            ):

                self.color_palette.get_color_clicked(x, y)
                self.update_colors()

            return None

        for button in self.menus[self.cur_menu]:

            if is_in(
                x,
                y,
                button.start_win_pos,
                button.end_win_pos,
            ):
                return button

        return None

    def update_colors(self) -> None:

        new_colors: list[tuple] = [
            self.maze.wall_color,
            self.maze.bg_color,
            self.maze.path_color,
            self.maze.entry_exit_color
        ]

        if self.cur_menu == "color_change":

            new_colors[0] = random.choice(
                random.choice(self.color_palette.colors).nuances
            )

            for color in range(1, 4):

                new_color = random.choice(
                    random.choice(self.color_palette.colors).nuances
                )
                while new_color in new_colors:
                    new_color = random.choice(
                        random.choice(self.color_palette.colors).nuances
                    )
                new_colors[color] = new_color

            self.maze.change_colors(new_colors)
            return None

        match self.color_type:

            case ColorType.WALL:
                color_to_change: int = 0

            case ColorType.BG:
                color_to_change = 1

            case ColorType.PATH:
                color_to_change = 2

            case ColorType.ENTRY_EXIT:
                color_to_change = 3

        new_colors[color_to_change] = self.color_palette.color_picked
        self.maze.change_colors(new_colors)

    def change_menu(self, button_clicked: Button) -> None:

        match button_clicked.name:

            case "generate new maze":
                self.cur_menu = "gen_algo_choice"

            case "path menu":
                self.cur_menu = "path_menu"

            case "change colors":
                self.cur_menu = "color_change"

            case "back to menu":
                self.cur_menu = "main"

            case "random colors":
                self.cur_menu = "color_change"
                self.update_colors()

            case "custom colors":
                self.cur_menu = "color_palette"
                self.color_type = ColorType.WALL

            case "rainbow mode on/off":
                self.cur_menu = "color_change"
                self.maze.activate_rainbow()

            case "toggle path on/off":
                self.cur_menu = "path_menu"
                self.maze.toggle_path_on_off()

            case "recursive backtracking":
                self.cur_menu = "main"
                self.maze.set_maze(rec_backtrack(
                    self.maze.maze.sz,
                    self.maze.maze.entry_point,
                    self.maze.maze.exit_point,
                    None
                ))
                self.maze.start_animation()

            case "a*":
                a_star(self.maze.maze)
                self.maze.toggle_path_on_off()

            case "wilson":
                self.cur_menu = "main"
                # wilson()

            case "random":
                self.cur_menu = "main"
                # random.choice([rec_backtrack, wilson])()

            case "ok":

                if self.color_type != ColorType.ENTRY_EXIT:

                    self.cur_menu = "color_palette"

                    if self.color_type == ColorType.WALL:
                        self.color_type = ColorType.BG

                    elif self.color_type == ColorType.BG:
                        self.color_type = ColorType.PATH

                    elif self.color_type == ColorType.PATH:
                        self.color_type = ColorType.ENTRY_EXIT

                else:
                    self.cur_menu = "color_change"

            case "exit window":
                self.clear_all_buttons()
                clear_all(
                    (self.mlx, self.mlx_ptr, self.mlx_win),
                    self.maze
                )

        if button_clicked.name in [
            "a*",
            "jump point search"
        ]:
            self.cur_menu = "path_menu"
            # start pathfinding animation

        self.update_button_title()

    def update_button_title(self) -> None:

        match self.cur_menu:

            case "main":
                self.button_title = "A-Maze-Ing Menu"

            case "color_change":
                self.button_title = "Choose a color mode option"

            case "gen_algo_choice":
                self.button_title = "Choose a generation algorithm"

            case "color_palette":

                self.button_title = self.color_type

    def clear_all_buttons(self) -> None:

        for menu in self.menus.values():

            clear_img(
                menu[0].not_clicked["img_data"][0],
                menu[0].img_sz[1],
                menu[0].not_clicked["img_data"][1]
            )
            self.mlx.mlx_destroy_image(
                self.mlx_ptr,
                menu[0].not_clicked["img"]
            )

            for button in menu:

                button.clean_img((
                    self.mlx,
                    self.mlx_ptr,
                    self.mlx_win
                ))

        for img in [self.ok_button.not_clicked, self.ok_button.clicked]:

            clear_img(
                img["img_data"][0],
                self.ok_button.img_sz[1],
                img["img_data"][1]
            )
            self.mlx.mlx_destroy_image(
                self.mlx_ptr,
                img["img"]
            )

        self.color_palette.clean_img()
