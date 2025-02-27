import qi

from src.ollama_agent import OllamaAgent

if __name__ == "__main__":
    app = qi.Application(["--qi-url=192.168.10.40"])
    app.start()

    session = app.session
    ollama_agent = OllamaAgent(session)
    
    session.registerService("OllamaAgent", ollama_agent)
    print("Service ready")

    app.run()