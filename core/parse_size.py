def parse_size(size_str):
    """Parse a size string like "8x16" into a tuple of two integers.

    Args:
        size_str (str): A string in the form "<width>x<height>".

    Returns:
        tuple[int, int]: The width and height values.

    Raises:
        TypeError: If size_str is not a string.
        ValueError: If the string is not in the expected format or contains non-integer values.
    """
    if not isinstance(size_str, str):
        raise TypeError("size_str must be a string")

    normalized = size_str.strip().lower()
    if "x" not in normalized:
        raise ValueError(f"Invalid size format: {size_str!r}")

    width_str, height_str = normalized.split("x", 1)
    try:
        width = int(width_str.strip())
        height = int(height_str.strip())
    except ValueError as exc:
        raise ValueError(f"Invalid size values: {size_str!r}") from exc

    return width, height
