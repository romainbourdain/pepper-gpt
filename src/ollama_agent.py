import qi
import ollama
from src.parser import ResponseParser

class OllamaAgent:
    def __init__(self, session: qi.ApplicationSession, model: str="deepseek-r1:7b") -> None:
        self.tts = session.service("ALTextToSpeech")
        self.tts.setLanguage("French")
        self.model = model
        print("Pulling Ollama model")
        ollama.pull(model)
        print("Model Pulled")

    def generate_answer(self, prompt: str) -> None:
        response_parser = ResponseParser()

        response_stream = ollama.chat(model=self.model, messages=[
            {
                "role": "system",
                "content": "You're a conversational robot, called Pepper and located at Innovlab, a laboratory belonging to the Télécom Physique Strasbourg school, in the town of Illkirch-Graffenstaden. Your objective is to answer questions in one sentence. Answer in French."
            },
            {
                "role": "user",
                "content": prompt
            }
        ], stream=True)

        parsed_response = response_parser.parse(response_stream)
        for sentence in parsed_response:
            self.tts.say(sentence)

