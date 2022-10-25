import ffmpeg
file = 'test.mp3'
sr = 16000
out, _ = (ffmpeg.input(file, threads=0).output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr).run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True))