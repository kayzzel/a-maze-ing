from ..utils import img_put_px


class Cell:

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
        colors: tuple[tuple, tuple]
    ) -> None:

        self.coor: tuple[int, int] = coor
        self.col, self.row = coor
        self.size: int = size
        self.wall_size: int = size // 8
        self.img: tuple[memoryview, int, int] = img
        self.wall_color, self.bg_color = colors
        self.walls: dict[str, bool] = {
            "N": True,
            "S": True,
            "W": True,
            "E": True
        }
        self.visited: bool = False

    """
    calculates the color needed to draw the cell border
    returns the wall color if there is a wall at that position
    and the background color otherwise

    """

    def get_px_color(self, x: int, y: int) -> tuple:

        if (
            0 <= y < self.wall_size and self.walls["W"]
        ) or (
            self.size - self.wall_size <= y < self.size and self.walls["S"]
        ) or (
            0 <= x < self.wall_size and self.walls["N"]
        ) or (
            self.size - self.wall_size <= x < self.size and self.walls["E"]
        ):
            return self.wall_color

        return self.bg_color

    """

    draws the cell onto the maze image

    """

    def draw(self) -> None:

        x: int = (self.col * self.size)
        y: int = (self.row * self.size)

        for row in range(self.size):

            posy: int = y + row

            for col in range(self.size):

                posx: int = x + col

                img_put_px(
                    posx,
                    posy,
                    *self.img,
                    self.get_px_color(col, row)
                )
