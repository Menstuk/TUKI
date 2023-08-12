from faster_whisper import WhisperModel
import logging

# logging.basicConfig()
# logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

model_size = "large-v2"

video_name = 'check1.M4A'
model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(video_name, beam_size=5)
# With VAD filter and an option to control the silence length to be removed 
# segments, _ = model.transcribe(
#     "audio.mp3",
#     vad_filter=True,
#     vad_parameters=dict(min_silence_duration_ms=500),
# )
# print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

segments = list(segments)  # The transcription will actually run here.
txt = ""
for segment in segments:
    txt = txt + segment.text

print(txt)
