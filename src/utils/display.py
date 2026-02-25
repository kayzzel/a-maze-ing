def img_put_px(
    x: int,
    y: int,
    buf: memoryview,
    sz_line: int,
    bpp: int,
    colors: tuple[int, int, int, int]
) -> None:

    offset = y * sz_line + x * (bpp // 8)
    for color in range(len(colors)):
        buf[offset + color] = colors[color]
