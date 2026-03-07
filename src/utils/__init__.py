from .mlx_display import (
    img_put_px,
    render,
    get_color_palette
)
from .events import handle_buttons, global_update
from .cleanup import clear_all, clear_img
from .checks import check_maze_input, compute_walls
__all__ = [
    "img_put_px",
    "get_color_palette",
    "handle_buttons",
    "global_update",
    "render",
    "clear_img",
    "clear_all",
    "check_maze_input",
    "compute_walls"
]
