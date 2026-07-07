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
        # CORREÇÃO 1: Forçando o motor nativo do Windows (sapi5)
        self.engine = pyttsx3.init('sapi5') 
        self.recognizer = sr.Recognizer()
        self._configurar_voz()
#======
# FALA
#======    
    def _configurar_voz(self):
        """Configura a voz imponente e tenta selecionar uma voz masculina."""
        self.engine.setProperty('rate', 140)  
        self.engine.setProperty('volume', 1.0)
        
        voices = self.engine.getProperty('voices')
        
        # CORREÇÃO 2: Trava de segurança. Só faz o loop se o Windows achou vozes.
        if voices:
            print("\n--- Vozes disponíveis no sistema ---")
            for i, voice in enumerate(voices):
                print(f"Voz {i}: {voice.name}")
            print("------------------------------------\n")

            try:
                # Lembre-se de mudar para voices[1].id se a 0 for feminina
                self.engine.setProperty('voice', voices[0].id)
                print(f"[Sistema] Voz selecionada: {voices[0].name}")
            except Exception as e:
                print(f"[Sistema] Erro ao configurar voz: {e}")
        else:
            print("[Sistema] ALERTA: O Windows não retornou nenhuma voz instalada. Usando voz padrão do sistema.")

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
            
                   