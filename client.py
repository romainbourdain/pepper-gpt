import qi

if __name__ == "__main__":
    app = qi.Application(["--qi-url=192.168.10.40"])
    app.start()

    session = app.session
    ollama_agent = session.service("OllamaAgent")

    ollama_agent.prompt = "Pourquoi le ciel est bleu ?"

    ollama_agent.generate_answer()