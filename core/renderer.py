import cv2
import numpy as np
from core.parse_size import parse_size


def render_image(
    frame,
    max_width,
    max_height,
    invert=False,
    block=False,
    color=True,
    only_char=None,
    square=False,
    size="8x16",
):
    # frame là numpy array (BGR)
    if frame is None or getattr(frame, "size", 0) == 0:
        return ""
    width_char, height_char = parse_size(size)
    aspect_ratio = frame.shape[0] / frame.shape[1]
    char_ratio = height_char / width_char

    if square:
        double = round(char_ratio)
        max_width //= double
        correction = 1
    else:
        double = 1
        correction = char_ratio
    target_width = min(max_width, int(max_height * correction / aspect_ratio))
    target_width = max(1, target_width)
    target_height = max(1, int(aspect_ratio * target_width / correction))

    # Choose interpolation method: INTER_NEAREST for pixel-perfect zoom, INTER_AREA for downsampling
    interpolation = cv2.INTER_NEAREST

    if color:
        # For color mode, always use solid block "█" with colors, no need for grayscale
        resized_color = cv2.resize(
            frame, (target_width, target_height), interpolation=interpolation
        )
        block = only_char[0] if only_char else "█"
        block = block * double  # Repeat character for square pixels if needed
        ascii_lines = [
            "".join(
                f"\033[38;2;{resized_color[y, x][2]};{resized_color[y, x][1]};{resized_color[y, x][0]}m{block}"
                for x in range(target_width)
            )
            + "\033[0m"
            for y in range(target_height)
        ]
    else:
        # For non-color mode, compute grayscale and ASCII chars
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if gray.shape[1] == 0:
            return ""
        default_chars = r""" .'\'`"^",:;I!il<>~+_?-[]{})1(|/\tfjrnxuvczXYUJCLQ0OZwmpqbdkhao*#MW&8%B@$"""
        block_chars = " ░▒▓█"
        if block:
            ascii_chars = block_chars
        else:
            ascii_chars = default_chars
        resized_gray = cv2.resize(
            gray, (target_width, target_height), interpolation=interpolation
        )

        # Vectorized ASCII character mapping using numpy
        pixel_values = resized_gray.astype(np.uint32)
        if invert:
            pixel_values = 255 - pixel_values
        indices = np.clip(
            pixel_values * len(ascii_chars) // 256, 0, len(ascii_chars) - 1
        )
        ascii_arr = np.fromiter(ascii_chars, dtype="<U1")
        char_grid = ascii_arr[indices]
        if double > 1:
            char_grid = np.repeat(char_grid, double, axis=1)
        ascii_lines = ["".join(char_grid[y]) for y in range(target_height)]

    return "\n".join(ascii_lines)
