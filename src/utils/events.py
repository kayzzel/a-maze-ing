from .cleanup import clear_all
from .mlx_display import render


"""

updates the maze and buttons each turn
then renders them to display them correctly on the window

"""


def global_update(param: tuple) -> None:

    buttons: list
    mlx_data: tuple
    maze, buttons, mlx_data = param

    for button in buttons:
        button.update()

    maze.animate_step()

    render(maze, buttons, mlx_data)


"""

handles all mouse events that happen during the mlx loop

"""


def handle_buttons(
    button_type: int,
    x: int,
    y: int,
    param: tuple
) -> None:

    buttons: list
    mlx_data: tuple
    buttons, maze, mlx_data = param

    # checks whether or not the mouse event is a left click

    if button_type != 1:
        return None

    button_pressed = None

    # checks if the mouse click is in the area of one of the buttons

    for button in buttons:

        if (
            button.base_pos[0] <= x < button.end_pos[0]
        ) and (
            button.base_pos[1] <= y < button.end_pos[1]
        ):
            button_pressed = button

    if not button_pressed:
        return None

    # starts and displays the clicking animation for the button pressed

    button_pressed.click_button()
    render(maze, buttons, mlx_data)

    # calls the appropriate function/method corresponding to the button action

    match button_pressed.name:

        case "Generate new maze":
            mlx_data[0].mlx_clear_window(mlx_data[1], mlx_data[2])
            for button in buttons:
                button.needs_refresh = True
            maze.start_animation()

        case "Toggle path on/off":
            maze.toggle_path_on_off()

        case "Change colors":
            maze.change_colors()

        case "Rainbow mode":
            maze.activate_rainbow()

        case "Exit window":
            clear_all(mlx_data, maze, buttons[0])
