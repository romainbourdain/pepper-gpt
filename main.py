from src.audio_transcriber import AudioTranscriber
from src.ollama_agent import OllamaAgent
from src.pepper_interface import PepperInterface

remote_audio_path = "/home/nao/recorded_audio.wav"
local_audio_path = "./audio/recorded_audio.wav"


def main() -> None:
    pepper_interface = PepperInterface()
    audio_transcriber = AudioTranscriber()
    ollama_agent = OllamaAgent()

    while True:
        user_input = input(
            "Appuyez sur Entrée pour enregistrer (ou 'exit' pour quitter) : "
        )

        if user_input.lower() in ["exit", "quit"]:
            print("Fin de la conversation. À bientôt !")
            break

        pepper_interface.record_audio(remote_audio_path)
        pepper_interface.download_audio(remote_audio_path, local_audio_path)
        transcription = audio_transcriber.transcribe(local_audio_path)

        for sentence in ollama_agent.chat_with_llm(transcription):
            pepper_interface.say(sentence)


if __name__ == "__main__":
    main()
