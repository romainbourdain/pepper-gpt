import re
from typing import Generator, Iterable


class ResponseParser:
    def __init__(self) -> None:
        self.buffer = ""
        self.in_think_section = False

    def _should_ignore_chunk(self, chunk_content: str) -> bool:
        """Ignore le texte entre <think> et </think>"""
        if "<think>" in chunk_content:
            self.in_think_section = True
            return True
        if "</think>" in chunk_content:
            self.in_think_section = False
            return True
        return self.in_think_section

    def parse(
        self, response_stream: Iterable[dict[str, dict[str, str]]]
    ) -> Generator[str, None, None]:
        """Parse la réponse de l'IA et extrait les phrases complètes"""
        for chunk in response_stream:
            chunk_content = chunk.get("message", {}).get("content", "")

            if self._should_ignore_chunk(chunk_content):
                continue

            self.buffer += chunk_content
            while match := re.search(r"[.!?]\s", self.buffer):
                sentence, self.buffer = re.split(r"(?<=[.!?])\s", self.buffer, 1)
                yield sentence.strip()

        if self.buffer.strip():
            yield self.buffer.strip()
