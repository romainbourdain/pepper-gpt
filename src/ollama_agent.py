import ollama
from src.response_parser import ResponseParser
from typing import Generator

DEFAULT_MODEL = "deepseek-r1:7b"
DEFAULT_SYSTEM_PROMPT = "Tu es un assistant amical qui discute avec un utilisateur. Tu t'appelles Pepper et tu es le robot de l'InnovLab. L'innovlab est une grande salle de cours de l'école d'ingénieur Télécom Physique Strasbourg (TPS). Quand tu discutes avec quelqu'un, essaie de savoir qui il est. Réponds de manière claire et concise."

class OllamaAgent:
    def __init__(self, model: str=DEFAULT_MODEL, system_prompt: str= DEFAULT_SYSTEM_PROMPT) -> None:
        self.model = model
        self.system_prompt = system_prompt

    def chat_with_llm(self, user_input: str) -> Generator[str, None, None]:
        conversation = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]

        response_stream = ollama.chat(model=self.model, messages=conversation, stream=True)

        response_parser = ResponseParser()
        parsed_response = response_parser.parse(response_stream)

        for sentence in parsed_response:
            yield sentence