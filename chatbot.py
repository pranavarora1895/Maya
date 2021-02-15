from chatterbot import ChatBot
from main import speak, takeCommand
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a Chatbot
chatbot = ChatBot('maya')


# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.english')
def chatting():
    while True:
        query = takeCommand()
        speak(chatbot.get_response(query))
        if "exit" in query:
            break
