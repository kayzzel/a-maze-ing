from .cleanup import clear_img


def img_put_px(
    x: int,
    y: int,
    buf: memoryview,
    sz_line: int,
    bpp: int,
    color: tuple[int, int, int, int]
) -> None:

    r: int
    g: int
    b: int
    a: int

    b, g, r, a = color

    offset = y * sz_line + x * (bpp // 8)

    buf[offset + 0] = r
    buf[offset + 1] = g
    buf[offset + 2] = b
    buf[offset + 3] = a


def generate_buttons(mlx_data: tuple, width: int) -> dict:

    posx = width - 300
    posy = 100

    buttons: dict[str, any] = {
        "Generate new maze": None,
        "Toggle path on/off": None,
        "Change colors": None,
        "Exit window": None
    }

    for button_name in buttons.keys():

        buttons[button_name] = draw_button(
            button_name,
            (posx, posy),
            *mlx_data
        )
        posy += 200

    return buttons


def draw_button(
    button_name: str,
    coor: tuple,
    mlx,
    mlx_ptr,
    mlx_win
) -> tuple[tuple]:

    button_sz: tuple = (len(button_name) * 10 + 50, 100)

    border = mlx.mlx_new_image(mlx_ptr, *button_sz)

    draw_border(*(mlx.mlx_get_data_addr(border)), button_sz)

    mlx.mlx_put_image_to_window(mlx_ptr, mlx_win, border, *coor)

    mlx.mlx_string_put(
        mlx_ptr,
        mlx_win,
        coor[0] + 25,
        coor[1] + 40,
        255,
        button_name
    )

    return (coor, (
        coor[0] + button_sz[0],
        coor[1] + button_sz[1]
    ))


def draw_border(
    buf: memoryview,
    bpp: int,
    sz_line: int,
    endian,
    button_sz: tuple
) -> None:

    clear_img(buf)

    for posy in range(button_sz[1]):

        for posx in range(button_sz[0]):

            if (
                posy < 2
            ) or (
                posy > button_sz[1] - 2
            ) or (
                posx < 2
            ) or (
                posx > button_sz[0] - 2
            ):
                img_put_px(
                    posx,
                    posy,
                    buf,
                    sz_line,
                    bpp,
                    (255, 255, 255, 255)
                )


def get_color_palette() -> tuple[tuple[tuple]]:

    return (
        (
            (0, 0, 255, 255),
            (255, 255, 255, 255),
            (255, 0, 0, 255)
        ),
        (
            (0, 255, 0, 255),
            (255, 255, 255, 255),
            (0, 0, 255, 255)
        ),
        (
            (255, 0, 0, 255),
            (255, 255, 255, 255),
            (0, 255, 0, 255)
        )
    )
