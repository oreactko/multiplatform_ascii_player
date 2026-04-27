import argparse
import re
import shutil
from core.renderer import render_image
ansi_escape = re.compile(r"\x1b\[[0-9;]*m")

def visible_length(s):
    return len(ansi_escape.sub("", s))

def parse_args():
    parser = argparse.ArgumentParser(description="Play Video from url in ASCII art with audio playback.")
    parser.add_argument("--vid", required=True, help="Video (can be URL or file path)")
    parser.add_argument("--audio", action="store_true", help="Play audio from video")
    parser.add_argument("--invert", action="store_true", help="Invert ASCII colors")
    parser.add_argument("--block", action="store_true", help="Use block characters for ASCII art")
    parser.add_argument(
        "--color",
        dest="color",
        action="store_true",
        help="Enable colored ASCII art.If enabled, it will automatically use '█' character and ignore --block",
    )
    parser.add_argument("--only-char", help="Use only the specified character for ASCII art (overrides --block).If use 1 character, it will automatically set color mode.")
    return parser.parse_args()

def print_centered_ascii(ascii_art, term_width, term_height):
    lines = ascii_art.splitlines()
    art_height = len(lines)
    art_width = max(visible_length(line) for line in lines) if lines else 0

    # Tính số dòng trống phía trên để căn giữa dọc
    pad_top = max((term_height - art_height) // 2, 0)
    # Tính số khoảng trắng bên trái để căn giữa ngang
    pad_left = max((term_width - art_width) // 2, 0)

    print("\n" * pad_top, end="")
    for line in lines:
        print(" " * pad_left + line)

def get_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def draw_frame(art,max_width, max_height):
    print("\033[H", end="")
    print_centered_ascii(art, max_width, max_height)