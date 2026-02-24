from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self as self


class MazeData(BaseModel):

    width: int = Field(ge=5, le=50)
    height: int = Field(ge=5, le=50)
    entry_coor: tuple[int, int]
    exit_coor: tuple[int, int]
    output_filename: str
    perfect: bool

    @model_validator(mode="after")
    def validate_coordinates(self) -> self:
        for coor in [self.entry_coor, self.exit_coor]:
            if not 0 <= coor[0] < self.width or not 0 <= coor[1] < self.height:
                raise ValueError("Invalid coordinates!")
        if self.entry_coor == self.exit_coor:
            raise ValueError("Entry and exit coordinates are the same!")
        return self

    @model_validator(mode="after")
    def validate_filename(self) -> self:
        if not self.output_filename.endswith(".txt"):
            raise ValueError("Invalid output filename (text file required)")
        return self

    def display_config_info(self) -> None:

        print("====  [MAZE CONFIGURATION]  ====\n")
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
