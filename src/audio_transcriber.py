from faster_whisper import WhisperModel


class AudioTranscriber:
    def __init__(
        self, model: str = "small", device: str = "cpu", compute_type: str = "int8"
    ) -> None:
        self.model = WhisperModel(model, device=device, compute_type=compute_type)

    def transcribe(self, file_path: str) -> str:
        segments, _ = self.model.transcribe(file_path)
        return " ".join(segment.text for segment in segments).strip()
