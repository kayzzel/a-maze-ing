from ..utils.mlx_display import img_put_px


class DisplayCell:
    """
        Description:
    A single maze cell that knows how to draw itself onto an MLX image.
    Each pixel is colored as either a wall or background depending on
    the cell's wall state and the pixel's position within the cell

        Parameters:
    coor -> the (col, row) coordinates of the cell inside the maze
    size -> the pixel size of the square cell
    img -> the maze image buffer as (buf, sz_line, bpp)
    colors -> a list of two RGBA tuples as [wall_color, bg_color]
    walls -> a dict mapping direction keys (N, S, E, W) to booleans,
             True if the wall is open, False if closed

        Attributes:
    coor -> the (col, row) coordinates of the cell
    col -> the column index of the cell
    row -> the row index of the cell
    sz -> the pixel size of the cell
    wall_sz -> the thickness of the walls in pixels, at least 1
    img -> the image buffer tuple
    wall_color -> the RGBA color used to draw walls
    bg_color -> the RGBA color used to draw the cell background
    walls -> the wall state dict for this cell
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
        # Ensure wall thickness is at least 1 pixel regardless of cell size
        self.wall_sz: int = self.sz // 8 if self.sz // 8 > 0 else 1
        self.img: tuple[memoryview, int, int] = img
        self.wall_color, self.bg_color = colors
        self.walls: dict[str, bool] = walls

    def get_px_color(self, x: int, y: int) -> tuple:
        """
            Description:
        Determine the color of a single pixel within the cell based on
        its local position. Returns the wall color if the pixel falls
        within a closed wall border, and the background color otherwise

            Parameters:
        x -> the local x position of the pixel within the cell
        y -> the local y position of the pixel within the cell

            Returns value:
        return the RGBA wall color if the pixel is on a closed wall,
        or the RGBA background color if it is in the interior
        """

        if 0 <= y < self.wall_sz and self.walls["N"]:
            return self.wall_color
        if self.sz - self.wall_sz <= y < self.sz and self.walls["S"]:
            return self.wall_color
        if 0 <= x < self.wall_sz and self.walls["W"]:
            return self.wall_color
        if self.sz - self.wall_sz <= x < self.sz and self.walls["E"]:
            return self.wall_color
        return self.bg_color

    def draw_cell(self) -> None:
        """
            Description:
        Draw the cell onto the maze image by iterating over every pixel
        in the cell's bounding square. Each pixel is first cleared and
        then colored according to get_px_color
        """

        # Compute the top-left pixel position of this cell in the image
        x: int = (self.col * self.sz)
        y: int = (self.row * self.sz)

        for row in range(self.sz):
            posy: int = y + row

            for col in range(self.sz):
                posx: int = x + col

                # Clear pixel before drawing to avoid color blending artifacts
                img_put_px(
                    posx,
                    posy,
                    *self.img,
                    (0, 0, 0, 0)
                )

                # Draw the pixel with its wall or background color
                img_put_px(
                    posx,
                    posy,
                    *self.img,
                    self.get_px_color(col, row)
                )
