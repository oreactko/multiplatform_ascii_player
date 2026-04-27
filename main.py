import cv2
from utils.get_path import get_video_path
from core.video import open_video
from cli import *
from core.audio import start_audio
from core.renderer import render_image
import time
args=parse_args()
video_path = get_video_path(args.vid)
cap, fps = open_video(video_path)
if args.audio:
    audio_time = start_audio(video_path)
else:
    start_time = time.monotonic()
try:
    while True:
        term_width, term_height = get_size()
        if args.audio:
            idx_frame = int(audio_time() * fps)
        else:
            idx_frame = int((time.monotonic() - start_time) * fps)
        idx_frame = max(idx_frame, 0)

        if term_width < 10 or term_height < 10:
            continue

        cap.set(cv2.CAP_PROP_POS_FRAMES, idx_frame)
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        ascii_art = render_image(
            frame,
            term_width,
            term_height,
            invert=args.invert,
            block=args.block,
            color=args.color,
            only_char=args.only_char
        )
        draw_frame(ascii_art, term_width, term_height)
except KeyboardInterrupt:
    pass
finally:
    cap.release()
