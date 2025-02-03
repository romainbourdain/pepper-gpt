import qi
import sys


app = qi.Application()
app.start()

s = app.session
ollama_answerer = s.service("ollama")

ollama_answerer.answer()