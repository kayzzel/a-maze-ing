from .mlx_display import render


# Maps keycodes to their corresponding values:
# digits 0-9, comma, space, enter, and delete
KEYS: dict[int, int | str] = {
    48 + index: index
    for index in range(10)
    } | {44: ",", 32: " ", 65293: "enter", 65288: "del"}


def global_update(param: tuple) -> None:
    """
        Description:
    Advance the maze animation by one step, update all button states,
    and render the current frame to the window. Called once per MLX
    loop iteration

        Parameters:
    param -> a tuple of (maze, button_menu, mlx_data) where maze is the
             MazeDisplay instance, button_menu is the ButtonMenu instance,
             and mlx_data is the (mlx, mlx_ptr, mlx_win) rendering context
    """

    mlx_data: tuple
    maze, button_menu, mlx_data = param

    maze.display_anim_step()
    button_menu.update_buttons()
    render(maze, button_menu, mlx_data)


def handle_buttons(
    button_type: int,
    x: int,
    y: int,
    param: tuple
) -> None:
    """
        Description:
    Handle a mouse click event by identifying which button was clicked,
    playing its click animation, and triggering the corresponding menu
    action. Ignores all non-left-click events

        Parameters:
    button_type -> the mouse button code, 1 for a left click
    x -> the x coordinate of the click in the window
    y -> the y coordinate of the click in the window
    param -> a tuple of (maze, button_menu, mlx_data)
    """

    mlx_data: tuple
    maze, button_menu, mlx_data = param

    # Ignore all mouse events that are not a left click
    if button_type != 1:
        return None

    button_pressed = button_menu.find_button_clicked(x, y)

    # Do nothing if the click did not land on any button
    if button_pressed:

        # Play the click animation then trigger the menu action
        button_pressed.click_button()
        render(maze, button_menu, mlx_data)
        button_menu.change_menu(button_pressed)


def handle_keyboard_input(
    keycode: int,
    param: tuple
) -> None:
    """
        Description:
    Handle a keyboard event during settings input. Enter confirms and
    submits the current input, delete removes the last character, and
    any other mapped key appends its value to the input buffer. Does
    nothing if the input widget is not currently active

        Parameters:
    keycode -> the keycode of the key that was pressed
    param -> a tuple of (button_menu, mlx_data)
    """

    button_menu, mlx_data = param

    # Ignore keyboard events when the input widget is not active
    if not button_menu.input.taking_input:
        return None

    if KEYS[keycode] == "enter":
        # Submit the current input to the settings handler
        button_menu.handle_settings()
        return None

    if KEYS[keycode] == "del":
        # Do nothing if there is no input to delete
        if not button_menu.input.user_input:
            return None
        button_menu.input.user_input.pop()

    else:
        # Append the pressed key's value to the input buffer
        button_menu.input.user_input.append(KEYS[keycode])

    # Redraw the input widget to reflect the updated buffer
    button_menu.input.update()
    button_menu.input.display_img_on_window()
