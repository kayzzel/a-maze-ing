from .mlx_display import render


KEYS: dict[int, int | str] = {
    48 + index: index
    for index in range(10)
} | {44: ",", 32: " ", 65293: "enter"}


"""

updates the maze and buttons each turn
then renders them to display them correctly on the window

"""


def global_update(param: tuple) -> None:

    mlx_data: tuple
    maze, button_menu, mlx_data = param

    maze.display_anim_step()

    button_menu.update_buttons()

    render(maze, button_menu, mlx_data)


"""

handles all mouse events that happen during the mlx loop

"""


def handle_buttons(
    button_type: int,
    x: int,
    y: int,
    param: tuple
) -> None:

    mlx_data: tuple
    maze, button_menu, mlx_data = param

    # checks whether or not the mouse event is a left click

    if button_type != 1:
        return None

    button_pressed = button_menu.find_button_clicked(x, y)

    # checks if the mouse click is in the area of one of the buttons

    if button_pressed:

        # starts and displays the clicking animation for the button pressed

        button_pressed.click_button()
        render(maze, button_menu, mlx_data)
        button_menu.change_menu(button_pressed)


def handle_keyboard_input(
    keycode: int,
    param: tuple
) -> None:

    button_menu, mlx_data = param

    if not button_menu.taking_input:
        return None

    if keycode not in KEYS.keys():
        return None

    if KEYS[keycode] == "enter":
        button_menu.handle_settings()
        return None

    button_menu.user_input.append(KEYS[keycode])
    # print(f"key: {keycode} - key type: {type(keycode).__name__}\n")
