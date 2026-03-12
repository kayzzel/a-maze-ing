from ..utils.mlx_display import img_put_px


class DisplayCell:

    """

    ---- initializing the cell ----

    [parameters needed]

     => hexa: the hexadecimal value that indicates the walls' state
     => coor: the coordinates of the cell inside the maze
     => size: the size of the square cell
     => img: the maze image to draw the cell on
     => colors: the wall color and background color

    [attributes of the class]

     => walls: 4 boolean values indicating the walls' state
            (True if open, False if closed)
     => wall_size: the thickness of the walls

    """

    def __init__(
        self,
        coor: tuple[int, int],
        size: int,
        img: tuple[memoryview, int, int],
        colors: list[tuple],
        walls: dict[str, bool]
    ) -> None:

        self.coor: tuple[int, int] = coor
        self.col, self.row = coor
        self.sz: int = size
        self.wall_sz: int = self.sz // 8 if self.sz // 8 > 0 else 1
        self.img: tuple[memoryview, int, int] = img
        self.wall_color, self.bg_color = colors
        self.walls: dict[str, bool] = walls

    """
    calculates the color needed to draw the cell border
    returns the wall color if there is a wall at that position
    and the background color otherwise

    """

    def get_px_color(self, x: int, y: int) -> tuple:

        if 0 <= y < self.wall_sz and self.walls["N"]:
            return self.wall_color

        if self.sz - self.wall_sz <= y < self.sz and self.walls["S"]:
            return self.wall_color

        if 0 <= x < self.wall_sz and self.walls["W"]:
            return self.wall_color

        if self.sz - self.wall_sz <= x < self.sz and self.walls["E"]:
            return self.wall_color

        return self.bg_color

    """

    draws the cell onto the maze image

    """

    def draw_cell(self) -> None:

        x: int = (self.col * self.sz)
        y: int = (self.row * self.sz)

        for row in range(self.sz):

            posy: int = y + row

            for col in range(self.sz):

                posx: int = x + col

                img_put_px(
                    posx,
                    posy,
                    *self.img,
                    (0, 0, 0, 0)
                )

                img_put_px(
                    posx,
                    posy,
                    *self.img,
                    self.get_px_color(col, row)
                )
