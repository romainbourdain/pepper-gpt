from faster_whisper import WhisperModel

class AudioTranscriber:
    def __init__(self, model="small", device="cpu", compute_type="int8"):
        self.model = WhisperModel(model, device=device, compute_type=compute_type)

    def transcribe(self, file_path):
        segments, _ = self.model.transcribe(file_path)
        transcription = " ".join(segment.text for segment in segments).strip()

        return transcription