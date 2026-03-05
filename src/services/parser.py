from ..models.maze_data import MazeData
from pydantic import ValidationError
from typing import Any as any
import re


def validate_format(line: str) -> tuple:

    if not (match := re.match("([A-Z_]+)=([a-zA-Z0-9.,]+)", line)):

        raise ValueError(
            f"Invalid format in configuration file!\nline: {line}"
        )

    if not match.group(1) in [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    ]:

        raise ValueError(
            f"Invalid key in configuration file! (key: '{match.group(1)}')"
        )

    if match.group(1) in ["WIDTH", "HEIGHT"]:

        value: int | str | list | tuple | bool = int(match.group(2))

    elif match.group(1) in ["ENTRY", "EXIT"]:

        value = match.group(2).split(",")
        value = tuple((int(value[0]), int(value[1])))

    elif match.group(1) == "PERFECT":

        value = bool(match.group(2))

    else:

        value = match.group(2)

    return (match.group(1).lower(), value)


def parse_config(config_filename: str) -> None | MazeData:

    config_data: dict[str, any] = {}

    try:

        with open(config_filename) as config:

            for line in config.readlines():

                new_pair: tuple = validate_format(line)

                if new_pair[0] in config_data.keys():

                    raise ValueError(
                        f"Data '{new_pair[0].upper()}' "
                        "has already been configured!"
                    )

                config_data[new_pair[0]] = new_pair[1]

        return MazeData(
            width=config_data["width"],
            height=config_data["height"],
            entry_coor=config_data["entry"],
            exit_coor=config_data["exit"],
            output_filename=config_data["output_file"],
            perfect=config_data["perfect"]
        )

    except ValidationError as err:

        print(f"Caught ValidationError: {err.errors()[0]['msg']}\n")

    except (ValueError, ValidationError, OSError) as err:

        print(f"Caught {err.__class__.__name__}: {err}\n")

    return None
