import re
from typing import Generator, Iterable

class ResponseParser:
    buffer: str
    in_think_section: bool

    def __init__(self) -> None:
        self.buffer: str = ""
        self.in_think_section: bool = False

    def _should_ignore_chunk(self, chunk_content : str) -> bool:
        if "<think>" in chunk_content:
            self.in_think_section = True
            return True
        if "</think>" in chunk_content:
            self.in_think_section = False
            return True
        return self.in_think_section

    def _extract_sentences(self) -> Generator[str, None, None]:
        while match := re.search(r"[.!?]\s", self.buffer):
            sentence, self.buffer = re.split(r"(?<=[.!?])\s", self.buffer, 1)
            yield sentence.strip()

    def parse(self, response_stream: Iterable[dict[str: any]]) -> Generator[str, None, None]:
        for chunk in response_stream:
            chunk_content = chunk.get("message", {}).get("content", "")

            if self._should_ignore_chunk(chunk_content):
                continue

            self.buffer += chunk_content
            yield from self._extract_sentences()
        
        if self.buffer.strip():
            yield self.buffer.strip()
