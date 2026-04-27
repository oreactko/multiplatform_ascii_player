from urllib.parse import urlparse
import yt_dlp
from pathlib import Path

def is_url(s):
    u = urlparse(s)
    return u.scheme in ("http", "https", "ftp") and u.netloc
def get_video_path(video_input:str) -> str:
    if not is_url(video_input):
        if Path(video_input).is_file():
            return video_input
        raise FileNotFoundError(f"File video không tồn tại: {video_input}")

    ydl_opts = {
        "format": "best[ext=mp4]/best",  # bắt buộc lấy mp4 (để OpenCV tương thích)
        "quiet": True,
        "no_warnings": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_input, download=False)
            path = info_dict["url"]
    except Exception as e:
        raise ValueError(
            "Không thể lấy link video trực tiếp. Có thể video này bị bảo vệ hoặc YouTube vừa thay đổi giao diện.",
            "Chi tiết lỗi:", e
        )    
    return path
