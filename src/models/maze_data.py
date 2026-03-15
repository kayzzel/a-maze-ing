from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self as self


class MazeData(BaseModel):
    """
        Description:
    A Pydantic model that holds and validates the configuration data
    for a maze. Ensures dimensions are within bounds, coordinates are
    valid and distinct, and the output filename has the correct extension

        Attributes:
    width -> the width of the maze in cells, between 5 and 50 inclusive
    height -> the height of the maze in cells, between 5 and 50 inclusive
    entry_coor -> the (col, row) coordinate of the maze entry point
    exit_coor -> the (col, row) coordinate of the maze exit point
    output_filename -> the path to the output file, must end with .txt
    perfect -> True if the maze should be a perfect maze (no loops)
    """

    width: int = Field(ge=5, le=50)
    height: int = Field(ge=5, le=50)
    entry_coor: tuple[int, int]
    exit_coor: tuple[int, int]
    output_filename: str
    perfect: bool

    @model_validator(mode="after")
    def validate_coordinates(self) -> self:
        """
            Description:
        Validate that both entry and exit coordinates lie within the maze
        bounds and that they are not the same point

            Returns value:
        return the validated MazeData instance if all checks pass,
        or raise a ValueError if any coordinate is out of bounds
        or the entry and exit are identical
        """

        # Ensure each coordinate is within the grid boundaries
        for coor in [self.entry_coor, self.exit_coor]:
            if not 0 <= coor[0] < self.width or not 0 <= coor[1] < self.height:
                raise ValueError("Invalid coordinates!")

        # Ensure the entry and exit are not placed on the same cell
        if self.entry_coor == self.exit_coor:
            raise ValueError("Entry and exit coordinates are the same!")

        return self

    @model_validator(mode="after")
    def validate_filename(self) -> self:
        """
            Description:
        Validate that the output filename ends with the .txt extension

            Returns value:
        return the validated MazeData instance if the filename is valid,
        or raise a ValueError if the extension is incorrect
        """

        if not self.output_filename.endswith(".txt"):
            raise ValueError("Invalid output filename (text file required)")

        return self

    def display_config_info(self) -> None:
        """
            Description:
        Print a formatted summary of the current maze configuration to
        stdout, listing each field name and its value
        """

        print("====  [MAZE CONFIGURATION]  ====\n")

        # Print each field name in uppercase alongside its current value
        for attr in [
            "width",
            "height",
            "entry_coor",
            "exit_coor",
            "output_filename",
            "perfect"
        ]:
            print(f"-> {attr.upper()}: {getattr(self, attr)}")

        print("")
