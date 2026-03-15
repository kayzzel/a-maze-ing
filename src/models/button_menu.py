from .button import Button
from .input import Input
from .maze_display import MazeDisplay
from .maze_generator import MazeGenerator
from .color_palette import ColorPalette
from ..utils.cleanup import clear_img, clear_all
from ..utils.checks import is_in
from ..utils.mlx_display import put_str_to_img
from ..services.generation_algo.rec_backtrack import rec_backtrack
from ..services.generation_algo.wilson import wilson
from ..services.solving_algo.a_star import a_star
from ..services.solving_algo.jump_point_search import jump_point_search
from enum import Enum
import random


class ColorType(str, Enum):

    WALL = "Wall Color"
    BG = "Background Color"
    PATH = "Path Color"
    ENTRY_EXIT = "Entry/Exit Color"


class ButtonTitle:

    def __init__(
        self,
        title: str,
        img_sz: tuple[int, int],
        img_pos: tuple[int, int],
        mlx_data: tuple
    ) -> None:

        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.img_sz: tuple[int, int] = img_sz
        self.img_pos: tuple[int, int] = img_pos

        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr,
            *img_sz
        )

        self.buf, self.bpp, self.sz_line, _ = self.mlx.mlx_get_data_addr(
            self.img
        )

        clear_img(self.buf, self.img_sz[1], self.sz_line)

        self.draw(title)

    def draw(self, title: str) -> None:

        clear_img(self.buf, self.img_sz[1], self.sz_line)

        put_str_to_img(
            title,
            self.buf,
            (
                (self.img_sz[0] - (len(title) * 12)) // 2,
                0
            ),
            self.sz_line,
            self.bpp,
            (255, 255, 255, 255)
        )

    def display(self) -> None:

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.mlx_win,
            self.img,
            *self.img_pos
        )


class ButtonMenu:

    def __init__(
        self,
        mlx_data: tuple,
        maze_display: MazeDisplay,
        generator: MazeGenerator,
        win_sz: tuple[int, int]
    ) -> None:

        self.mlx, self.mlx_ptr, self.mlx_win = mlx_data
        self.maze: MazeDisplay = maze_display
        self.generator: MazeGenerator = generator
        self.win_sz: tuple[int, int] = win_sz

        self.menus: dict[str, list[Button]] = {
            "start_menu": self.generate_buttons([
                "maze",
                "settings",
                "exit window"
            ]),
            "main": self.generate_buttons([
                "generate new maze",
                "path menu",
                "change colors",
                "back to main menu"
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
                "random",
                "back to menu"
            ]),
            "path_menu": self.generate_buttons([
                "a*",
                "jump point search",
                "toggle path on/off",
                "back to menu"
            ]),
            "skip": self.generate_buttons(["skip"]),
            "settings": self.generate_setting_buttons([
                f"maze width : {self.generator.get_maze_sz()[0]}",
                f"maze height : {self.generator.get_maze_sz()[1]}",
                f"perfect : {self.generator.get_perfect()}",
                "back to main menu",
                f"seed : {self.generator.get_seed()}",
                f"entry point : {self.generator.get_entry_exit_point()[0]}",
                f"exit point : {self.generator.get_entry_exit_point()[1]}"
            ])
        }

        self.color_palette: ColorPalette = ColorPalette(
            mlx_data,
            win_sz
        )

        self.create_ok_button()

        self.cur_menu: str = "start_menu"
        self.prev_menu: str = ""

        self.initialize_button_title()

        self.color_type: ColorType

        self.input: Input = Input(win_sz, mlx_data)

        self.start_menu_img, _, _ = self.mlx.mlx_xpm_file_to_image(
                self.mlx_ptr, "./src/images/start_menu.xpm"
                )

        self.menus["main"][0].needs_refresh = True
        self.display_button_menu()

    def initialize_button_title(self) -> None:

        self.button_title: ButtonTitle = ButtonTitle(
            "A Maze Ing Menu",
            (self.win_sz[0], 30),
            (
                0,
                self.maze.img_pos[1] + self.maze.img_height + 30
            ),
            (self.mlx, self.mlx_ptr, self.mlx_win)
        )

    def update_buttons(self) -> None:

        self.ok_button.update()

        for menu in self.menus.values():

            for button in menu:

                button.update()

        if self.cur_menu == "skip" and not self.maze.animating:

            self.change_menu(self.menus["skip"][0])
            self.menus["skip"][0].needs_refresh = True
            self.display_button_menu()

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

        if not self.cur_menu == "settings":
            self.button_title.display()

        if self.cur_menu == "start_menu" and self.start_menu_img:
            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr, self.mlx_win,
                self.start_menu_img,
                (self.win_sz[0] - 800) // 2,
                self.win_sz[1] // 10
            )

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

        if self.input.taking_input:

            self.input.update()
            self.input.display_img_on_window()
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

    def generate_setting_buttons(self, settings: list[str]) -> list[Button]:

        lines: list[list[str]] = [
            settings[:2],
            settings[2:len(settings) - 2],
            settings[len(settings) - 2:]
        ]

        button_height: int = self.win_sz[1] // 7

        setting_buttons: list[Button] = []

        for line in range(len(lines)):

            button_width: int = (
                (self.win_sz[0] - len(lines[line])) // 2
            )
            if button_width > 400:
                button_width = 400

            horizontal_offset: int = (
                self.win_sz[0] - len(lines[line]) * button_width
            ) // (len(lines[line]) + 1)

            for button_number in range(len(lines[line])):

                button_pos: tuple[int, int] = (
                    (
                        button_width * button_number
                        + horizontal_offset * (button_number + 1)
                    ),
                    (self.win_sz[1] // 7) * (line + 1)
                    + button_height * line
                )

                setting_buttons.append(Button(
                    lines[line][button_number],
                    (button_width, button_height),
                    button_pos,
                    (255, 255, 255, 255),
                    self.win_sz,
                    (0, 0)
                ))

        self.render_button_images(setting_buttons)

        return setting_buttons

    def refresh_setting(self, setting: Button) -> None:

        if setting is None:
            return None

        setting.click_button()

        if "width" in setting.name:
            setting.name = (
                "maze width : "
                f"{self.generator.get_maze_sz()[0]}"
            )

        elif "height" in setting.name:
            setting.name = (
                "maze height : "
                f"{self.generator.get_maze_sz()[1]}"
            )

        elif "entry" in setting.name:
            setting.name = (
                "entry point : "
                f"{self.generator.get_entry_exit_point()[0]}"
            )

        elif "exit" in setting.name:
            setting.name = (
                "exit point : "
                f"{self.generator.get_entry_exit_point()[1]}"
            )

        elif "perfect" in setting.name:
            setting.name = (
                "perfect : "
                f"{self.generator.get_perfect()}"
            )

        elif "seed" in setting.name:
            setting.name = f"seed : {self.generator.get_seed()}"

        buf = self.menus["settings"][0].not_clicked["img_data"][0]
        height = self.menus["settings"][0].img_sz[1]
        sz_line = self.menus["settings"][0].not_clicked["img_data"][1]

        clear_img(buf, height, sz_line)

        for setting_button in self.menus["settings"]:

            setting_button.draw(
                self.menus["settings"][0].not_clicked["img_data"],
                0
            )

        # rendering all the pressed button images

        for s in range(len(self.menus["settings"])):

            # initializing a new image for each button

            buf = self.menus["settings"][s].clicked["img_data"][0]
            height = self.menus["settings"][s].img_sz[1]
            sz_line = self.menus["settings"][s].clicked["img_data"][1]
            clear_img(buf, height, sz_line)

            for setting_nb in range(len(self.menus["settings"])):

                # setting the offset to draw the button
                # at the correct position on the image

                offset: int = 0

                if setting_nb == s:
                    offset = 2

                self.menus["settings"][setting_nb].draw(
                    self.menus["settings"][setting_nb].clicked["img_data"],
                    offset
                )

    """

    generates all the buttons needed for the display

    """

    def generate_buttons(self, button_names: list[str]) -> list[Button]:

        button_img_sz: tuple[int, int] = (
            self.win_sz[0],
            self.win_sz[1] // 8 + 100
        )
        button_image_pos: tuple[int, int] = (
            0,
            self.maze.img_pos[1] + self.maze.img_height + 100
        )

        buttons: list[Button] = []

        button_width: int = (
            self.win_sz[0] // len(button_names)
            - (100 - 10 * len(button_names))
        )
        button_height: int = self.win_sz[1] // 8

        if button_width > 300:
            button_width = 300

        if button_height > 150:
            button_height = 150

        if button_names[0] == "skip" and button_width > 400:
            button_width = 400

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

        if not self.cur_menu:
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

            case "skip":
                self.cur_menu = self.prev_menu
                self.maze.stop_animation()

            case "maze":
                self.cur_menu = "main"
                self.maze.set_new_maze(
                    self.generator.initialize_maze()
                )

            case "settings":
                self.cur_menu = "settings"

            case "generate new maze":
                self.cur_menu = "gen_algo_choice"

            case "path menu":
                self.cur_menu = "path_menu"

            case "change colors":
                self.cur_menu = "color_change"

            case "back to main menu":
                self.cur_menu = "start_menu"
                if self.maze.toggle_path:
                    self.maze.toggle_path_on_off()
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.maze.generated = False
                self.input.reset()

            case "back to menu":
                self.cur_menu = "main"

            case "random colors":
                self.cur_menu = "color_change"
                self.update_colors()

            case "custom colors":
                self.color_type = ColorType.WALL
                self.cur_menu = "color_palette"

            case "rainbow mode on/off":
                self.cur_menu = "color_change"
                self.maze.activate_rainbow()

            case "toggle path on/off":
                self.cur_menu = "path_menu"
                if not self.maze.toggle_path:
                    self.generator.solve_algo(self.maze.maze)
                self.maze.toggle_path_on_off()

            case "recursive backtracking":
                self.cur_menu = "skip"
                self.prev_menu = "gen_algo_choice"
                self.maze.toggle_path = False
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.generator.gen_algo = rec_backtrack
                self.maze.set_new_maze(self.generator.generate_maze())
                self.maze.start_animation()

            case "wilson":
                self.cur_menu = "skip"
                self.prev_menu = "gen_algo_choice"
                self.maze.toggle_path = False
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.generator.gen_algo = wilson
                self.maze.set_new_maze(self.generator.generate_maze())
                self.maze.start_animation()

            case "a*":
                self.cur_menu = "skip"
                self.prev_menu = "path_menu"
                if self.maze.toggle_path:
                    self.maze.toggle_path_on_off()
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.generator.solve_algo = a_star
                self.generator.solve_algo(self.maze.maze)
                self.maze.toggle_path_on_off(True)

            case "jump point search":
                self.cur_menu = "skip"
                self.prev_menu = "path_menu"
                if self.maze.toggle_path:
                    self.maze.toggle_path_on_off()
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                jump_point_search(self.maze.maze)
                self.maze.toggle_path_on_off(True)

            case "random":
                self.cur_menu = "skip"
                self.prev_menu = "gen_algo_choice"
                self.maze.toggle_path = False
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.generator.gen_algo = random.choice([
                    wilson, rec_backtrack
                ])
                self.maze.set_new_maze(self.generator.generate_maze())
                self.maze.start_animation()
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

        if "perfect" in button_clicked.name:

            self.generator.set_perfect(not self.generator.get_perfect())
            self.refresh_setting(button_clicked)

        elif button_clicked.name in [
            button.name
            for button in self.menus["settings"]
            if button.name != "back to main menu"
        ]:
            self.input.taking_input = True
            self.input.cur_setting = button_clicked
            self.cur_menu = ""

        if self.maze.animating and not self.maze.rainbow_mode:
            self.cur_menu = "skip"

        self.update_button_title()

    def update_button_title(self) -> None:

        match self.cur_menu:

            case "start_menu":
                self.button_title.draw("A Maze Ing Menu")

            case "settings":
                self.button_title.draw("")

            case "main":
                self.button_title.draw("Maze Menu")

            case "color_change":
                self.button_title.draw("Choose a color mode option")

            case "gen_algo_choice":
                self.button_title.draw("Choose a generation algorithm")

            case "skip":
                self.button_title.draw("")

            case "color_palette":

                self.button_title.draw(self.color_type)

    def handle_settings(self) -> None:

        if not (
            self.input.taking_input
            and self.input.cur_setting
            and self.input.user_input
        ):
            self.input.reset()
            return None

        try:
            if (
                "maze width" in self.input.cur_setting.name
                or "maze height" in self.input.cur_setting.name
            ):

                if not all(
                    isinstance(nb, int)
                    for nb in self.input.user_input
                ):
                    raise ValueError

                val = 0

                for value in self.input.user_input:
                    val = val * 10 + value

                if "width" in self.input.cur_setting.name:
                    new_sz: tuple[int, int] = (
                        val,
                        self.generator.get_maze_sz()[1]
                    )
                else:
                    new_sz = (
                        self.generator.get_maze_sz()[0],
                        val
                    )

                self.generator.set_maze_sz(new_sz)

            elif (
                "entry point" in self.input.cur_setting.name
                or "exit point" in self.input.cur_setting.name
            ):

                if not all(
                    value in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ","]
                    for value in self.input.user_input
                ):
                    raise ValueError

                new_x: int = 0
                new_y: int = 0
                comma_encountered: bool = False

                for value in self.input.user_input:

                    if value != "," and not comma_encountered:
                        new_x = new_x * 10 + value

                    elif value != "," and comma_encountered:
                        new_y = new_y * 10 + value

                    elif value == "," and not comma_encountered:
                        comma_encountered = True

                    elif value == "," and comma_encountered:
                        raise ValueError

                print(
                    self.input.cur_setting.name.split(
                        " :", 1
                    )[0].replace(" point", "")
                )
                self.generator.set_entry_exit_point(
                    (new_x, new_y),
                    self.input.cur_setting.name.split(
                        " :", 1
                    )[0].replace(" point", "")
                )

            elif "seed" in self.input.cur_setting.name:

                if not all(
                    isinstance(nb, int)
                    for nb in self.input.user_input
                ):
                    if not all(
                        isinstance(letter, str)
                        for letter in self.input.user_input
                    ):
                        raise ValueError
                    elif "".join(self.input.user_input) == "none":
                        val = None
                    else:
                        raise ValueError

                else:
                    val = 0

                    for value in self.input.user_input:
                        val = val * 10 + value

                self.generator.set_seed(val)

        except ValueError:
            self.input.user_input = list("Invalid input, please try again")
            self.input.update()
            self.input.display_img_on_window()
            self.input.user_input = []
            self.input.taking_input = True
            return None

        self.cur_menu = "settings"
        self.refresh_setting(self.input.cur_setting)
        self.input.reset()

    def clear_all_buttons(self) -> None:

        if self.start_menu_img:
            self.mlx.mlx_destroy_image(self.mlx_ptr, self.start_menu_img)

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
        self.input.clean_img()
