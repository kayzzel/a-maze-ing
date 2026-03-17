from ..models.maze_data import MazeData
from pydantic import ValidationError
from typing import Any as any
import re


def validate_format(line: str) -> tuple:
    """
        Description:
    Validate a single line from the configuration file and parse it into
    a key-value pair. The line must follow the format KEY=value, the key
    must be one of the accepted configuration keys, and the value is cast
    to the appropriate type depending on the key

        Parameters:
    line -> a single line string read from the configuration file

        Returns value:
    return a tuple of (key, value) where key is the lowercased config key
    and value is cast to int, tuple, bool, or str depending on the key
    """

    # Ensure the line matches the expected KEY=value format
    if not (match := re.match("([A-Z_]+)=([a-zA-Z0-9.,]+)", line)):
        raise ValueError(
            f"Invalid format in configuration file!\nLine: {line}"
        )

    # Ensure the key is one of the accepted configuration keys
    if not match.group(1) in [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"
    ]:
        raise ValueError(
            f"Invalid key in configuration file! (key: '{match.group(1)}')"
        )

    # Cast the value to the appropriate type based on the key
    if match.group(1) in ["WIDTH", "HEIGHT"]:

        if not match.group(2).isnumeric():
            raise ValueError(
                f"Invalid value {match.group(2)} for "
                "maze width or height"
            )

        value: int | str | list | tuple | bool | None = int(match.group(2))

    elif match.group(1) in ["ENTRY", "EXIT"]:
        # Split the coordinate string and convert to a tuple of ints
        value = match.group(2).split(",")

        if len(value) != 2:
            raise ValueError(
                "Too many values provided for "
                "entry/exit coordinates (only two required)"
            )

        if not value[0].isnumeric() or not value[1].isnumeric():
            raise ValueError(
                f"Invalid coordinates {value} provided (must be integers)"
            )

        value = tuple((int(value[0]), int(value[1])))

    elif match.group(1) == "PERFECT":

        if match.group(2) not in ["True", "False"]:
            raise ValueError(
                f"Invalid value {match.group(2)} for perfection parameter "
                "(must be a boolean)"
            )

        value = bool(match.group(2))

    elif match.group(1) == "SEED":

        if not match.group(2).isnumeric() and match.group(2) != "None":
            raise ValueError(
                f"Invalid value {match.group(2)} for seed "
                "(must be an integer or None)"
            )

        if match.group(2) == "None":
            value = None

        else:
            value = int(match.group(2))

    elif match.group(1) == "OUTPUT_FILE":

        value = match.group(2)

    return (match.group(1).lower(), value)


def parse_config(config_filename: str) -> None | MazeData:
    """
        Description:
    Read and parse a maze configuration file, validate each key-value pair,
    and return a MazeData instance populated with the parsed values.
    Lines starting with '#' are treated as comments and ignored

        Parameters:
    config_filename -> the path to the configuration file to parse

        Returns value:
    return a MazeData instance if the file is valid and all required fields
    are present, or None if any error is encountered during parsing
    """

    config_data: dict[str, any] = {}

    try:
        with open(config_filename) as config:
            for line in config.readlines():

                # Skip comment lines
                if line.startswith("#") or line.strip() == "":
                    continue

                # Parse the line into a key-value pair and check for duplicates
                new_pair: tuple = validate_format(line)
                if new_pair[0] in config_data.keys():
                    raise ValueError(
                        f"Data '{new_pair[0].upper()}' "
                        "has already been configured!"
                    )

                # Store the validated key-value pair
                config_data[new_pair[0]] = new_pair[1]

        if not all(
            key in config_data.keys()
            for key in [
                "width",
                "height",
                "entry",
                "exit",
                "output_file",
                "perfect",
                "seed"
            ]
        ):
            raise KeyError("Missing keys in configuration file")
        # Build and return the MazeData from the collected configuration values
        return MazeData(
            width=config_data["width"],
            height=config_data["height"],
            entry_point=config_data["entry"],
            exit_point=config_data["exit"],
            output_filename=config_data["output_file"],
            perfect=config_data["perfect"],
            seed=config_data["seed"]
        )

    # Handle Pydantic validation errors separately for a cleaner error message
    except ValidationError as err:
        print(f"Caught ValidationError: {err.errors()[0]['msg']}\n")
    except (ValueError, ValidationError, OSError, KeyError) as err:
        print(f"Caught {err.__class__.__name__}: {err}\n")

    return None
