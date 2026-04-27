import ffmpeg
import pyaudio
import threading

def start_audio(video_url):
    # Truyền video dạng bytes vào ffmpeg (stdin), và nhận audio mp3 qua stdout
    probe = ffmpeg.probe(video_url)
    audio_stream = next((s for s in probe["streams"] if s["codec_type"] == "audio"), None)
    if audio_stream is None:
        raise ValueError("No audio stream found in video")

    sample_rate = int(audio_stream["sample_rate"])
    channels = int(audio_stream["channels"])
    process = (
        ffmpeg.input(video_url)  # đọc từ stdin
        .output(
            "pipe:1", format="s16le", acodec="pcm_s16le", ac=channels, ar=sample_rate
        )
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=channels, rate=sample_rate, output=True
    )

    frames_played = 0
    bytes_per_frame = 2 * channels
    chunk = 4096

    # Dùng AudioSegment để phát
    def audio_thread():
        nonlocal frames_played
        while True:
            data = process.stdout.read(chunk)
            if not data:
                break
            stream.write(data)
            frames_played += len(data) // bytes_per_frame

        stream.stop_stream()
        stream.close()
        p.terminate()

    def burn_stderr():
        while True:
            data = process.stderr.read(1024)
            if not data:
                break

    t = threading.Thread(target=audio_thread)
    burn = threading.Thread(target=burn_stderr)
    t.daemon = True
    burn.daemon = True
    t.start()
    burn.start()

    def get_audio_time():
        latency = stream.get_output_latency()
        return frames_played / sample_rate - latency

    return get_audio_time