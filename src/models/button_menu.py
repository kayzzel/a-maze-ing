from .button import Button
from .input import Input
from .maze_display import MazeDisplay
from .maze_generator import MazeGenerator
from .color_palette import ColorPalette
from ..utils.cleanup import clear_img, clear_all
from ..utils.checks import is_in
from ..services.generation_algo.rec_backtrack import rec_backtrack
from ..services.generation_algo.wilson import wilson
from ..services.solving_algo.a_star import a_star
from ..services.solving_algo.jump_point_search import jump_point_search
from enum import Enum
import random


class ColorType(str, Enum):
    """
        Description:
    An enumeration of the four color types that can be customized
    in the maze display. Used to track which color is currently
    being edited in the color palette menu

        Attributes:
    WALL -> the color of the maze walls
    BG -> the background color of the maze
    PATH -> the color of the solution path
    ENTRY_EXIT -> the color of the entry and exit points
    """

    WALL = "Wall Color"
    BG = "Background Color"
    PATH = "Path Color"
    ENTRY_EXIT = "Entry/Exit Color"


class ButtonMenu:
    """
        Description:
    Manages all the button menus of the application, including rendering,
    navigation between menus, user input handling, color selection,
    maze generation and solving, and settings configuration

        Parameters:
    mlx_data -> a tuple containing (mlx, mlx_ptr, mlx_win) for the MLX instance
    maze_display -> the MazeDisplay instance used to render the maze
    generator -> the MazeGenerator instance used to generate and solve mazes
    win_sz -> the size of the window as (width, height)

        Attributes:
    mlx, mlx_ptr, mlx_win -> the MLX rendering context
    maze -> the MazeDisplay instance
    generator -> the MazeGenerator instance
    win_sz -> the window size
    menus -> a dict mapping menu names to their list of Buttons
    color_palette -> the ColorPalette widget used for custom color picking
    ok_button -> the confirmation button used in the color palette menu
    cur_menu -> the name of the currently active menu
    prev_menu -> the name of the previously active menu, used for back navigation
    button_title -> the title string displayed above the current menu
    color_type -> the ColorType currently being edited in the color palette
    input -> the Input instance used to collect user settings input
    """

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

        # Build all menus by generating their buttons
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
                "maze width",
                "maze height",
                "perfect",
                "back to main menu",
                "seed",
                "entry point",
                "exit point"
            ])
        }

        self.color_palette: ColorPalette = ColorPalette(
            mlx_data,
            win_sz
        )

        self.create_ok_button()

        self.cur_menu: str = "start_menu"
        self.prev_menu: str = ""

        self.button_title: str = "A-Maze-Ing Menu"

        self.color_type: ColorType

        self.input: Input = Input(win_sz, mlx_data)

        # Mark the first main menu button as needing a refresh and render
        self.menus["main"][0].needs_refresh = True
        self.display_button_menu()

    def update_buttons(self) -> None:
        """
            Description:
        Update the state of all buttons and the ok button. If the skip menu
        is active and the maze has finished animating, switch back to the
        previous menu and trigger a redisplay
        """

        self.ok_button.update()

        for menu in self.menus.values():

            for button in menu:

                button.update()

        # If the skip screen is showing and animation has ended, return to the previous menu
        if self.cur_menu == "skip" and not self.maze.animating:

            self.change_menu(self.menus["skip"][0])
            self.menus["skip"][0].needs_refresh = True
            self.display_button_menu()

    def needs_refresh(self) -> bool:
        """
            Description:
        Check whether any button in any menu or the ok button
        has been marked as needing a visual refresh

            Returns value:
        return True if at least one button needs a refresh, False otherwise
        """

        for menu in self.menus.values():

            if any(
                button.needs_refresh
                for button in menu
            ) or self.ok_button.needs_refresh:
                return True

        return False

    def display_button_menu(self) -> None:
        """
            Description:
        Clear the window and render the current menu. If the color palette
        menu is active it renders the palette and the ok button. If user
        input is being collected it renders the input widget instead.
        Otherwise it renders the buttons of the current menu, highlighting
        whichever button is currently pressed
        """

        if not self.needs_refresh():
            return None

        self.mlx.mlx_clear_window(self.mlx_ptr, self.mlx_win)

        # self.display_button_title()

        if self.cur_menu == "color_palette":

            self.color_palette.display_img()

            # Show the pressed or unpressed state of the ok button
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

        # Default to showing the unclicked state of the menu image
        img_to_display = menu_to_display[0].not_clicked

        # Switch to the clicked image if any button in the menu is pressed
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
        """
            Description:
        Render the current menu title string centered above the button area.
        Does nothing if button_title is empty
        """

        if self.button_title:

            self.mlx.mlx_string_put(
                self.mlx_ptr,
                self.mlx_win,
                (self.win_sz[0] - (len(self.button_title) * 10)) // 2,
                self.maze.img_pos[1] + self.maze.img_height + 25,
                0xFFFFFF,
                self.button_title
            )

    def create_ok_button(self) -> None:
        """
            Description:
        Instantiate and render the ok button used to confirm color
        selection in the color palette menu. The button is positioned
        to the right of the palette, vertically centered
        """

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
        """
            Description:
        Generate and render the buttons for the settings menu. The settings
        are arranged across three rows, with each row's buttons evenly spaced
        horizontally within the window

            Parameters:
        settings -> the list of setting names to create buttons for

            Returns value:
        return the list of rendered Button instances for the settings menu
        """

        # Split the settings into three rows
        lines: list[list[str]] = [
            settings[:2],
            settings[2:len(settings) - 2],
            settings[len(settings) - 2:]
        ]

        button_height: int = self.win_sz[1] // 7

        setting_buttons: list[Button] = []

        for line in range(len(lines)):

            # Compute the button width and horizontal spacing for this row
            button_width: int = (
                (self.win_sz[0] - len(lines[line])) // 2
            )
            if button_width > 400:
                button_width = 400

            horizontal_offset: int = (
                self.win_sz[0] - len(lines[line]) * button_width
            ) // (len(lines[line]) + 1)

            for button_number in range(len(lines[line])):

                # Compute the position of each button within its row
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

    def generate_buttons(self, button_names: list[str]) -> list[Button]:
        """
            Description:
        Generate and render all the buttons for a standard menu. Buttons are
        evenly spaced horizontally across the window and sized relative to
        the number of buttons and the window dimensions

            Parameters:
        button_names -> the list of button label strings to create

            Returns value:
        return the list of rendered Button instances for the menu
        """

        button_img_sz: tuple[int, int] = (
            self.win_sz[0],
            self.win_sz[1] // 8 + 100
        )
        button_image_pos: tuple[int, int] = (
            0,
            self.maze.img_pos[1] + self.maze.img_height + 100
        )

        buttons: list[Button] = []

        # Compute button dimensions, capping at maximum sizes
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

        # Compute the horizontal spacing between buttons
        horizontal_offset: int = (
            self.win_sz[0] - len(button_names) * button_width
        ) // (len(button_names) + 1)

        # Initialize each button with the correct values
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
        """
            Description:
        Render the MLX images for a list of buttons. One shared image is
        created for the unclicked state of all buttons, and one individual
        image is created per button for its clicked state, with that button
        drawn at a slight offset to indicate it is pressed

            Parameters:
        buttons -> the list of Button instances to render images for
        """

        # Render the shared image where no button is pressed
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

        # Assign the shared unclicked image to every button
        for button in buttons:

            button.not_clicked = {
                "img": none_clicked_img,
                "img_data": (buf, sz_line, bpp)
            }

        # Render one individual clicked image per button
        for b in range(len(buttons)):

            # Initialize a fresh image for this button's clicked state
            clicked_img = self.mlx.mlx_new_image(
                self.mlx_ptr,
                *buttons[0].img_sz
            )
            buf, bpp, sz_line, _ = self.mlx.mlx_get_data_addr(
                clicked_img
            )
            clear_img(buf, buttons[0].img_sz[1], sz_line)

            for button_nb in range(len(buttons)):

                # Draw the active button with an offset to simulate a press,
                # all other buttons are drawn at the normal position
                offset: int = 0

                if button_nb == b:
                    offset = 2

                buttons[button_nb].draw(
                    (buf, sz_line, bpp),
                    offset
                )

            # Assign the clicked image to the corresponding button
            buttons[b].clicked = {
                "img": clicked_img,
                "img_data": (buf, sz_line, bpp)
            }

    def find_button_clicked(self, x: int, y: int) -> Button | None:
        """
            Description:
        Determine which button was clicked at the given window coordinates.
        If the color palette menu is active, check the ok button and the
        palette itself. Otherwise check all buttons in the current menu

            Parameters:
        x -> the x coordinate of the click in the window
        y -> the y coordinate of the click in the window

            Returns value:
        return the Button that was clicked, or None if no button was hit
        """

        if self.cur_menu == "color_palette":

            # Check if the ok button was clicked
            if is_in(
                x,
                y,
                self.ok_button.start_win_pos,
                self.ok_button.end_win_pos
            ):
                return self.ok_button

            # Check if a color in the palette was clicked and update colors
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
        """
            Description:
        Update the maze colors based on the current menu context. If called
        from the color_change menu, four distinct random colors are picked
        from the palette. Otherwise the color corresponding to the current
        color_type is replaced with the color selected in the palette
        """

        new_colors: list[tuple] = [
            self.maze.wall_color,
            self.maze.bg_color,
            self.maze.path_color,
            self.maze.entry_exit_color
        ]

        if self.cur_menu == "color_change":

            # Pick four distinct random colors for all color slots
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

        # Map the current color type to its index in the colors list
        match self.color_type:

            case ColorType.WALL:
                color_to_change: int = 0

            case ColorType.BG:
                color_to_change = 1

            case ColorType.PATH:
                color_to_change = 2

            case ColorType.ENTRY_EXIT:
                color_to_change = 3

        # Replace only the targeted color slot with the palette selection
        new_colors[color_to_change] = self.color_palette.color_picked
        self.maze.change_colors(new_colors)

    def change_menu(self, button_clicked: Button) -> None:
        """
            Description:
        Handle a button click by navigating to the appropriate menu and
        triggering any associated actions such as starting maze generation,
        running a solving algorithm, changing colors, or updating settings

            Parameters:
        button_clicked -> the Button instance that was clicked
        """

        match button_clicked.name:

            case "skip":
                # Return to the previous menu and stop any running animation
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
                # Reset the maze state and input before returning to the start
                self.cur_menu = "start_menu"
                if self.maze.generated:
                    self.maze.stop_animation()
                    self.maze.generated = False
                    clear_img(
                        self.maze.buf,
                        self.maze.img_height,
                        self.maze.sz_line
                    )
                self.input.reset()

            case "settings":
                self.cur_menu = "settings"

            case "back to menu":
                self.cur_menu = "main"

            case "random colors":
                self.cur_menu = "color_change"
                self.update_colors()

            case "custom colors":
                # Enter the palette starting from the wall color
                self.cur_menu = "color_palette"
                self.color_type = ColorType.WALL

            case "rainbow mode on/off":
                self.cur_menu = "color_change"
                self.maze.activate_rainbow()

            case "toggle path on/off":
                self.cur_menu = "path_menu"
                self.maze.toggle_path_on_off()

            case "recursive backtracking":
                # Start maze generation using recursive backtracking and show skip
                self.cur_menu = "skip"
                self.prev_menu = "gen_algo_choice"
                self.maze.toggle_path = False
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.generator.gen_algo = rec_backtrack
                self.maze.set_new_maze(self.generator.generate_maze())
                self.maze.start_animation()

            case "wilson":
                # Start maze generation using Wilson's algorithm and show skip
                self.cur_menu = "skip"
                self.prev_menu = "gen_algo_choice"
                self.maze.toggle_path = False
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                self.generator.gen_algo = wilson
                self.maze.set_new_maze(self.generator.generate_maze())
                self.maze.start_animation()

            case "a*":
                # Solve the maze using A* and display the path
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
                # Solve the maze using Jump Point Search and display the path
                self.cur_menu = "skip"
                self.prev_menu = "path_menu"
                if self.maze.toggle_path:
                    self.maze.toggle_path_on_off()
                if self.maze.rainbow_mode:
                    self.maze.activate_rainbow()
                jump_point_search(self.maze.maze)
                self.maze.toggle_path_on_off(True)

            case "random":
                # Pick a random generation algorithm and start generation
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

                    # Advance to the next color type in the palette flow
                    self.cur_menu = "color_palette"

                    if self.color_type == ColorType.WALL:
                        self.color_type = ColorType.BG

                    elif self.color_type == ColorType.BG:
                        self.color_type = ColorType.PATH

                    elif self.color_type == ColorType.PATH:
                        self.color_type = ColorType.ENTRY_EXIT

                else:
                    # All colors have been picked, return to the color menu
                    self.cur_menu = "color_change"

            case "exit window":
                # Clean up all button images before closing the window
                self.clear_all_buttons()
                clear_all(
                    (self.mlx, self.mlx_ptr, self.mlx_win),
                    self.maze
                )

        # Toggle the perfect maze setting if that button was clicked
        if button_clicked.name == "perfect":

            self.generator.set_perfect(not self.generator.get_perfect())

        # Start text input collection for any editable settings button
        if button_clicked.name in [
            button.name
            for button in self.menus["settings"]
            if button.name not in ["perfect", "back to main menu"]
        ]:
            self.input.taking_input = True
            self.input.cur_setting = button_clicked

        # Switch to the path menu after a solving algorithm has been run
        if button_clicked.name in [
            "a*",
            "jump point search"
        ]:
            self.cur_menu = "path_menu"
            # start pathfinding animation

        # If an animation is running outside rainbow mode, show the skip menu
        if self.maze.animating and not self.maze.rainbow_mode:
            self.cur_menu = "skip"

        self.update_button_title()

    def update_button_title(self) -> None:
        """
            Description:
        Update the button_title string to match the currently active menu.
        The title is displayed above the buttons to indicate which menu
        the user is in
        """

        match self.cur_menu:

            case "start_menu":
                self.button_title = "A-Maze-Ing Menu"

            case "settings":
                self.button_title = ""

            case "main":
                self.button_title = "Maze Menu"

            case "color_change":
                self.button_title = "Choose a color mode option"

            case "gen_algo_choice":
                self.button_title = "Choose a generation algorithm"

            case "skip":
                self.button_title = ""

            case "color_palette":
                # Display the name of the color currently being edited
                self.button_title = self.color_type

    def handle_settings(self) -> None:
        """
            Description:
        Process the user input collected for a settings field. Parses and
        validates the input based on which setting is being edited, then
        applies the new value to the generator. Resets the input state and
        returns to the settings menu on success, or prompts the user to
        retry on invalid input

        """

        if not (
            self.input.taking_input
            and self.input.cur_setting
            and self.input.user_input
        ):
            self.input.reset()
            return None

        try:
            if self.input.cur_setting.name in ["maze width", "maze height"]:

                # Ensure all entered characters are integers
                if not all(
                    isinstance(nb, int)
                    for nb in self.input.user_input
                ):
                    raise ValueError

                # Reconstruct the full integer value digit by digit
                val = 0

                for value in self.input.user_input:
                    val = val * 10 + value

                if self.input.cur_setting.name == "maze width":
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

            elif self.input.cur_setting.name in ["entry point", "exit point"]:

                # Ensure all characters are digits or a single comma separator
                if not all(
                    value in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ","]
                    for value in self.input.user_input
                ):
                    raise ValueError

                new_x: int = 0
                new_y: int = 0
                comma_encountered: bool = False

                # Parse the x and y values separated by a comma
                for value in self.input.user_input:

                    if value != "," and not comma_encountered:
                        new_x = new_x * 10 + value

                    elif value != "," and comma_encountered:
                        new_y = new_y * 10 + value

                    elif value == "," and not comma_encountered:
                        comma_encountered = True

                    elif value == "," and comma_encountered:
                        # A second comma is invalid
                        raise ValueError

                self.generator.set_entry_exit_point(
                    (new_x, new_y),
                    self.input.cur_setting.name.replace(" point", "")
                )

            elif self.input.cur_setting.name == "seed":

                # Ensure all entered characters are integers
                if not all(
                    isinstance(nb, int)
                    for nb in self.input.user_input
                ):
                    raise ValueError

                # Reconstruct the full seed value digit by digit
                val = 0

                for value in self.input.user_input:
                    val = val * 10 + value

                self.generator.set_seed(val)

        except ValueError:
            # Notify the user of invalid input and allow them to retry
            self.input.input_title = "Invalid input, please try again"
            self.input.user_input = []
            self.input.taking_input = True
            return None

        # Reset the input state and return to the settings menu
        self.input.reset()
        self.cur_menu = "settings"
        self.menus["settings"][0].needs_refresh = True
        self.display_button_menu()

    def clear_all_buttons(self) -> None:
        """
            Description:
        Release all MLX images associated with every button in every menu,
        as well as the ok button and the color palette and input widgets.
        Should be called before closing the window to avoid memory leaks
        """

        for menu in self.menus.values():

            # Clear and destroy the shared unclicked image for this menu
            clear_img(
                menu[0].not_clicked["img_data"][0],
                menu[0].img_sz[1],
                menu[0].not_clicked["img_data"][1]
            )
            self.mlx.mlx_destroy_image(
                self.mlx_ptr,
                menu[0].not_clicked["img"]
            )

            # Clean up the individual clicked images for each button
            for button in menu:

                button.clean_img((
                    self.mlx,
                    self.mlx_ptr,
                    self.mlx_win
                ))

        # Clean up both images of the ok button
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
