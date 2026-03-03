from .display import generate_buttons
from .cleanup import clear_all


def handle_buttons(
    button: int,
    x: int,
    y: int,
    param: tuple
) -> None:

    buttons: dict[str, tuple]
    mlx_data: tuple
    buttons, maze, mlx_data = param

    if button != 1:
        return None

    button_pressed: str = ""

    for button_name, button_coor in buttons.items():
        if (
            button_coor[0][0] <= x < button_coor[1][0]
        ) and (
            button_coor[0][1] <= y < button_coor[1][1]
        ):
            button_pressed = button_name

    if not button_pressed:
        return None

    mlx_data[0].mlx_clear_window(mlx_data[1], mlx_data[2])

    match button_pressed:

        case "Generate new maze":
            maze.display_maze()
        case "Toggle path on/off":
            maze.toggle_path_on_off()
        case "Change colors":
            maze.change_colors()
        case "Exit window":
            maze.clear_img()
            clear_all(*mlx_data)

    generate_buttons(
        mlx_data,
        1000
    )
