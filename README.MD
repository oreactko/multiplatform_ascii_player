# Multi-Platform ASCII Player

## Giới thiệu

Multi-Platform ASCII Player là một project nhỏ để phát các video trên nhiều nền tảng video.

## Mục đích

- Hiển thị video dưới dạng ASCII art trong terminal.
- Hỗ trợ nhiều nền tảng và định dạng video(như YouTube, Vimeo, tệp cục bộ) với sự trợ giúp của yt-dlp.

## TODO

- [x] Hỗ trợ màu sắc trong ASCII art.
- [x] Tối ưu hóa performance cho terminal lớn.(dù chưa thực sự tối ưu được nhiều)
- [ ] Thêm mục tìm kiếm đa nền tảng(hiện tại sẽ chưa develop do tài khoản của tôi là tài khoản được giám sát nên không thể tạo API cho YouTube,nhưng sẽ có thể develop trước cho 1 số nền tảng khác).
- [ ] Viết hướng dẫn cài đặt và sử dụng chi tiết.

## Usage

```bash
    >python main.py --help
    usage: main.py [-h] --vid VID [--audio] [--invert] [--block] [--color]
                [--only-char ONLY_CHAR]

    Play Video from url in ASCII art with audio playback.

    options:
    -h, --help            show this help message and exit
    --vid VID             Video (can be URL or file path)
    --audio               Play audio from video
    --invert              Invert ASCII colors
    --block               Use block characters for ASCII art
    --color               Enable colored ASCII art.If enabled, it will
                            automatically use '█' or only-char and ignore --block
    --only-char ONLY_CHAR
                            Use only the specified character for ASCII art
                            (overrides --block).Requires --color.
```