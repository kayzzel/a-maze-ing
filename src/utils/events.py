from .cleanup import clear_all
from .display import render


def global_update(param: tuple) -> None:

    maze, buttons, *mlx_data = param

    for button in buttons:
        button.update()

    maze.animate_step()
    render(maze, buttons, mlx_data)


def handle_buttons(
    button: int,
    x: int,
    y: int,
    param: tuple
) -> None:

    buttons: list
    mlx_data: tuple
    buttons, maze, mlx_data = param

    if button != 1:
        return None

    button_pressed = None

    for button in buttons:

        if (
            button.base_pos[0] <= x < button.end_pos[0]
        ) and (
            button.base_pos[1] <= y < button.end_pos[1]
        ):
            button_pressed = button
            button.click_button()

    if not button_pressed:
        return None

    match button_pressed.name:

        case "Generate new maze":
            maze.start_animation()
        case "Toggle path on/off":
            maze.toggle_path_on_off()
        case "Change colors":
            maze.change_colors()
        case "Exit window":
            maze.clear_img()
            clear_all(*mlx_data)
