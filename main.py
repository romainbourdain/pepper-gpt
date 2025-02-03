from src.parser import ResponseParser

if __name__ == "__main__":
    response_stream =  [{"message": {"content": "Bonjour. Comment ça va ?"}},
             {"message": {"content": "Je vais bien, merci !"}}]
    parser = ResponseParser()
    parsed_sentences = list(parser.parse(response_stream))
    print(parsed_sentences)