import qi
import sys
import ollama
from parse_response import parse_response

class OllamaAnswerer:
    def __init__(self, session : qi.ApplicationSession):
        self.tts = session.service("ALTextToSpeech")
        print("Pulling Ollama model")
        ollama.pull("deepseek-r1:7b")
        print("Model pulled")

    def answer(self) -> None:
        response_stream = ollama.chat(model="deepseek-r1:7b", messages=[
            {
                "role": "system",
                "content": "You're a conversational robot, called Pepper and located at innovlab, a laboratory belonging to the Télécom Physique Strasbourg school, in the town of Illkirch Graffenstaden. Your objective is to answer questions in one sentence. Answer in French."
            },
            {
                "role": "user",
                "content": "Qui es-tu ?"
            }
        ], stream=True)

        formatted_response_stream = parse_response(response_stream)
        # for chunk in formatted_response_stream:
        #     print(chunk)


if __name__ == "__main__":
    app = qi.Application()
    app.start()

    session = app.session

    ollama_answerer = OllamaAnswerer(session)

    session.registerService("ollama", ollama_answerer)
    print("Service ready")

    app.run()