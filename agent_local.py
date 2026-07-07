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
#======
# FALA
#======    
    def _configurar_voz(self):
        """Configura a voz robótica e imponente do Agente"""
        self.engine.setProperty('rate', 140) # Voz mais cadenciada e imponente.
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        try:
            self.engine.setProperty('voice', voices[0].id)  # Seleciona o índice da voz (Muda para voices[1].id se a 0 for feminina)
        except Exception:
            pass

    def falar(self, texto):
        """Transforma o texto em áudio e reproduz no PC."""
        print(f"\n🤖 {ASSISTANT_NAME}: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()       
#========
# AUDIÇÃO
#========        
    def ouvir(self):
        """Capta o áudio do microfone e transforma em texto nativamente."""
        with sr.Microphone() as source:
            print("\n[Ajustar ruído ambiente...]")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"🎤 Estou a ouvir... (Diz 'Desligar' para encerrar)")
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                texto = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f"🗣️ Tu disseste: {texto}")
                return texto.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("🤔 Não consegui entender o áudio.")
                return ""
            except sr.RequestError:
                print("🌐 Falha na ligação de rede.")
                return ""