import whisper
model = whisper.load_model("base")
# result = model.transcribe("準備したファイル名を指定") # 今回の記事ではtest.m4aを用います。
path = "audio/codcall.mp3"
result = model.transcribe(path, language='en')
print(result["text"])
# I got a cold call from an insurance company yesterday.