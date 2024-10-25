from freechatbot import G4FChatbot
import g4f

class BaseProcessor:
    def __init__(self,filepath):
        self.fp = filepath
        self.chatbot = G4FChatbot(g4f.models.gpt_4o)
