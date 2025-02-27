from src.ollama_agent import OllamaAgent
from src.pepper_interface import PepperInterface
from src.audio_transcriber import AudioTranscriber
from dotenv import load_dotenv

remote_audio_path = "/home/nao/recorded_audio.wav"
local_audio_path = "./audio/recorded_audio.wav"

def main() -> None:
    load_dotenv()
    
    pepper_interface = PepperInterface()
    audio_transcriber = AudioTranscriber()
    ollama_agent = OllamaAgent()

    while True:
        user_input = input("Appuyez sur Entrée pour enregistrer (ou 'exit' pour quitter) : ")

        if user_input.lower() in ["exit", "quit"]:
            print("Fin de la conversation. À bientôt !")
            break

        pepper_interface.record_audio(remote_audio_path)
        pepper_interface.download_audio(remote_audio_path, local_audio_path)
        transcription = audio_transcriber.transcribe(local_audio_path)

        stream_response = ollama_agent.chat_with_llm(transcription)

        for sentence in stream_response:
            pepper_interface.say(sentence)

if __name__ == "__main__":
    main()
