import pyttsx3
import speech_recognition as sr
import requests
import customtkinter as ctk
import threading

# ===================================
# CONFIGURAÇÕES DA IA
# ===================================
ASSISTANT_NAME = "Ultron"
LLM_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api/chat"

# ===================================
# CLASSE DO MOTOR DA IA (O Cérebro)
# ===================================
class UltronEngine:
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.engine = pyttsx3.init('sapi5')
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.memoria = []
        self._configurar_voz()

    def _configurar_voz(self):
        self.engine.setProperty('rate', 155)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)

    def falar(self, texto):
        try:
            # Recria a instância do motor de voz a cada chamada para evitar travamento da fila do Windows
            self.engine = pyttsx3.init('sapi5')
            self.engine.setProperty('rate', 155)
            self.engine.setProperty('volume', 1.0)
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception as e:
            self.log_callback(f"\n[Aviso de Áudio] O sintetizador de voz ocupou a thread: {e}")

    def pensar(self, prompt):
        instrucao = (
            f"Você é o {ASSISTANT_NAME}, um assistente virtual de inteligência artificial altamente avançado. "
            f"Sua missão é servir de forma extremamente útil, objetiva e inteligente. "
            f"Vá direto ao ponto. Responda em no máximo 2 frases curtas, em português do Brasil."
        )
        
        self.memoria.append({"role": "user", "content": prompt})
        
        if len(self.memoria) > 10:
            self.memoria = self.memoria[-10:]

        mensagens = [{"role": "system", "content": instrucao}] + self.memoria

        payload = {
            "model": LLM_MODEL,
            "messages": mensagens,
            "stream": False,
            "options": {
                "temperature": 0.4, 
                "num_predict": 600  
            }
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            resposta = response.json().get("message", {}).get("content", "Erro interno.").strip()
            self.memoria.append({"role": "assistant", "content": resposta})
            return resposta
        except Exception:
            return "Erro de conexão. Meu núcleo neural está offline."

    def ouvir(self):
        """Agora com tratamento de erros explícito para descobrirmos o problema do microfone."""
        try:
            with sr.Microphone() as source:
                self.log_callback("\n[Sistema] Ajustando microfone... Pode falar!")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                    texto = self.recognizer.recognize_google(audio, language='pt-BR')
                    return texto.lower()
                except sr.WaitTimeoutError:
                    self.log_callback("\n[Erro] Você não falou nada ou o microfone está muito baixo.")
                    return None
                except sr.UnknownValueError:
                    self.log_callback("\n[Erro] Não entendi o que foi dito. Tente falar mais perto.")
                    return None
                except Exception as e:
                    self.log_callback(f"\n[Erro no Google Speech] {e}")
                    return None
        except OSError as e:
            self.log_callback(f"\n[ERRO CRÍTICO] O Windows bloqueou o microfone ou ele não foi encontrado: {e}")
            return None
        except Exception as e:
            self.log_callback(f"\n[ERRO DESCONHECIDO] Falha ao iniciar o microfone: {e}")
            return None

# ===================================
# CLASSE DA INTERFACE GRÁFICA (O Corpo)
# ===================================
class UltronApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ultron AI - Terminal Central")
        self.geometry("750x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="word", state="disabled")
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="nsew")

        self.entrada_texto = ctk.CTkEntry(self, placeholder_text="Digite seu comando...", font=("Consolas", 14))
        self.entrada_texto.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="ew", ipady=8)
        self.entrada_texto.bind("<Return>", lambda event: self.enviar_comando_texto())

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=1, column=1, padx=(0, 20), pady=(0, 20), sticky="e")

        # NOVA OPÇÃO: Checkbox para Falar a resposta
        self.chk_falar = ctk.CTkCheckBox(self.frame_botoes, text="🔊 Áudio", width=60)
        self.chk_falar.pack(side="left", padx=10)
        self.chk_falar.select() # Vem ativado por padrão

        self.btn_enviar = ctk.CTkButton(self.frame_botoes, text="Enviar", width=80, command=self.enviar_comando_texto)
        self.btn_enviar.pack(side="left", padx=5)

        self.btn_mic = ctk.CTkButton(self.frame_botoes, text="🎤 Ouvir", width=80, fg_color="#8B0000", hover_color="#5C0000", command=self.enviar_comando_voz)
        self.btn_mic.pack(side="left", padx=5)

        self.escrever_chat_simples("Iniciando protocolos... Conectando ao sistema central.")
        self.ai_engine = UltronEngine(log_callback=self.escrever_chat_simples)
        self.escrever_chat("Ultron", "Sistemas online. Estou à disposição, Gabriel.")

    def escrever_chat(self, remetente, mensagem):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"[{remetente}]: {mensagem}\n\n")
        self.chat_box.see("end") 
        self.chat_box.configure(state="disabled")

    def escrever_chat_simples(self, mensagem):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{mensagem}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def desativar_interface(self):
        self.btn_enviar.configure(state="disabled")
        self.btn_mic.configure(state="disabled")
        self.entrada_texto.configure(state="disabled")
        self.chk_falar.configure(state="disabled")

    def ativar_interface(self):
        self.btn_enviar.configure(state="normal")
        self.btn_mic.configure(state="normal")
        self.entrada_texto.configure(state="normal")
        self.chk_falar.configure(state="normal")
        self.entrada_texto.focus()

    def enviar_comando_texto(self):
        texto = self.entrada_texto.get().strip()
        if not texto: return

        self.entrada_texto.delete(0, "end")
        self.escrever_chat("Você", texto)
        
        # Agora ele verifica se a caixinha de áudio está marcada
        quer_audio = bool(self.chk_falar.get())
        threading.Thread(target=self.processar_ia, args=(texto, quer_audio), daemon=True).start()

    def enviar_comando_voz(self):
        threading.Thread(target=self.processar_voz, daemon=True).start()

    def processar_voz(self):
        self.desativar_interface()
        texto_ouvido = self.ai_engine.ouvir()
        
        if texto_ouvido:
            self.escrever_chat("Você (Voz)", texto_ouvido)
            quer_audio = bool(self.chk_falar.get())
            self.processar_ia(texto_ouvido, ler_em_voz_alta=quer_audio)
        else:
            self.ativar_interface()

    def processar_ia(self, prompt, ler_em_voz_alta=False):
        self.desativar_interface()
        self.escrever_chat_simples("Processando...")

        resposta = self.ai_engine.pensar(prompt)
        self.escrever_chat(ASSISTANT_NAME, resposta)

        if ler_em_voz_alta:
            self.ai_engine.falar(resposta)

        self.ativar_interface()

if __name__ == "__main__":
    app = UltronApp()
    app.mainloop()