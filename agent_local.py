import pyttsx3
import speech_recognition as sr
import requests

#===================================
# SETUP INICIAL E CONSTANTES GLOBAIS 
#===================================
ASSISTANT_NAME = "Ultron"
LLM_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api/generate"

class UltronAgent:
    def __init__(self):
        """Inicializa os motores de voz e reconhecimento."""
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self._configurar_voz()

#==============
# MOTOR DA VOZ
#==============        
    def _configurar_voz(self):
        """Configura a voz robótica e imponente do Agente"""
        self.engine.setProperty('rate', 140) # Voz mais cadenciada e imponente.
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        try:
            self.engine.setProperty('voice', voices[0].id)  # Índice da voz masculina padrão no Windows
        except Exception:
            pass

    def falar(self, texto):
        """Transforma o texto em áudio e reproduz no PC."""
        print(f"\n {ASSISTANT_NAME}: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()
        
   