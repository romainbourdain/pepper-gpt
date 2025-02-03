import pytest
from src.parser import ResponseParser


@pytest.mark.parametrize(
    "response_stream, expected_sentences",
    [
        (
            [{"message": {"content": "Bonjour. Comment ça va ?"}},
             {"message": {"content": "Je vais bien, merci !"}}],
            ["Bonjour.", "Comment ça va ?", "Je vais bien, merci !"]
        ),

        (
            [{"message": {"content": "Bonjour. <think>Je réfléchis...</think>"}},
             {"message": {"content": "Comment vas-tu ?"}}],
            ["Bonjour.", "Comment vas-tu ?"]
        ),

        (
            [{"message": {"content": "Ceci est une phrase incomplète"}},
             {"message": {"content": " mais maintenant elle est terminée."}}],
            ["Ceci est une phrase incomplète mais maintenant elle est terminée."]
        ),

        (
            [{"message": {"content": "C'est incroyable ! Vraiment ? Oui, totalement."}}],
            ["C'est incroyable !", "Vraiment ?", "Oui, totalement."]
        ),

        (
            [],
            []
        )
    ]
)
def test_response_parser(response_stream, expected_sentences):
    """Teste le parsing de réponses en streaming."""
    parser = ResponseParser()
    parsed_sentences = list(parser.parse(response_stream))
    assert parsed_sentences == expected_sentences