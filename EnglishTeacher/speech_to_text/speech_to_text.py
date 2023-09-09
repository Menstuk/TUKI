from faster_whisper import WhisperModel


class SpeechToText:
    def __init__(self, model_size="large-v2", device="cpu", temperature=0):
        self.temperature = temperature
        self.model_size = model_size
        self.model = WhisperModel(self.model_size, device=device, compute_type="int8")

    def get_transcription(self, audio):
        segments, _ = self.model.transcribe(audio=audio, beam_size=5, language='en', temperature=self.temperature)
        segments = list(segments)  # The transcription will actually run here.
        txt = ""
        for segment in segments:
            txt = txt + segment.text
        return txt
