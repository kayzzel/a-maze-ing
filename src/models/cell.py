from src.utils import img_put_px


class Cell:

    def __init__(
        self,
        hexa: str,
        coor: tuple[int, int],
        size: int,
        img: tuple[memoryview, int, int],
        colors: tuple[tuple, tuple]
    ) -> None:

        self.walls: tuple[
            bool, bool, bool, bool
        ] = self.compute_walls(hexa)
        self.coor: tuple[int, int] = coor
        self.size: int = size
        self.wall_size: int = size // 8
        self.img: tuple[memoryview, int, int] = img
        self.colors: tuple[tuple, tuple] = colors

    @staticmethod
    def compute_walls(hexa: str) -> tuple[bool, bool, bool, bool]:

        bin_val: str = bin(int(hexa, 16))[2:]

        if not len(bin_val) == 4:

            bin_val = "0" * (4 - len(bin_val)) + bin_val

            if not all(char in ["0", "1"] for char in bin_val):
                raise ValueError(
                    f"Cannot compute walls with invalid value '{hexa}'!"
                )

        return (
            bin_val[0] == "1",
            bin_val[1] == "1",
            bin_val[2] == "1",
            bin_val[3] == "1"
        )

    def get_px_color(self, x: int, y: int) -> tuple:

        if (
            0 <= y < self.wall_size and self.walls[3]
        ) or (
            self.size - self.wall_size <= y < self.size and self.walls[1]
        ) or (
            0 <= x < self.wall_size and self.walls[0]
        ) or (
            self.size - self.wall_size <= x < self.size and self.walls[2]
        ):
            return self.colors[0]

        return self.colors[1]

    def draw(self) -> None:

        x: int = (self.coor[0] * self.size)
        y: int = (self.coor[1] * self.size)

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
