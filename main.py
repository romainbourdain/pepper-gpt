from src.ollama_agent import OllamaAgent
import qi

if __name__ == "__main__":
    app = qi.Application(["--qi-url=192.168.10.40"])
    app.start()

    session = app.session
    ollama_agent = OllamaAgent(session)

    ollama_agent.generate_answer("Pourquoi Prégaldiny est-il chauve")