def is_in(
    x: int,
    y: int,
    start_pos: tuple[int, int],
    end_pos: tuple[int, int]
) -> bool:

    if (
        start_pos[0] <= x < end_pos[0]
    ) and (
        start_pos[1] <= y < end_pos[1]
    ):
        return True

    return False
