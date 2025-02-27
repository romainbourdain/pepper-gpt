from typing import Generator

import ollama

from src.const import DEFAULT_MODEL, DEFAULT_SYSTEM_PROMPT
from src.response_parser import ResponseParser


class OllamaAgent:
    def __init__(
        self, model: str = DEFAULT_MODEL, system_prompt: str = DEFAULT_SYSTEM_PROMPT
    ) -> None:
        self.model = model
        self.system_prompt = system_prompt
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt},
        ]

    def chat_with_llm(self, user_input: str) -> Generator[str, None, None]:
        self.conversation_history.append({"role": "user", "content": user_input})

        try:
            response_stream = ollama.chat(
                model=self.model, messages=self.conversation_history, stream=True
            )
            response_parser = ResponseParser()
            parsed_response = response_parser.parse(response_stream)

            for sentence in parsed_response:
                self.conversation_history.append(
                    {"role": "assistant", "content": sentence}
                )
                yield sentence
        except Exception as e:
            print(f"❌ Erreur lors de la communication avec Ollama : {e}")
