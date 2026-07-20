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
        self.log_callback = log_callback # Função para enviar texto para o ecrã
        self.engine = pyttsx3.init('sapi5')
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.memoria = []
        self._configurar_voz()

    def _configurar_voz(self):
        self.engine.setProperty('rate', 155)
        self.engine.setProperty('volume', 1.0)
        # Tenta colocar uma voz masculina ou a padrão
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)

    def falar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

    def pensar(self, prompt):
        instrucao = f"Você é o {ASSISTANT_NAME}, uma IA sarcástica. Responde sempre em português do Brasil, de forma ácida, curta e direta."
        self.memoria.append({"role": "user", "content": prompt})
        
        if len(self.memoria) > 10:
            self.memoria = self.memoria[-10:]

        mensagens = [{"role": "system", "content": instrucao}] + self.memoria

        payload = {
            "model": LLM_MODEL,
            "messages": mensagens,
            "stream": False,
            "options": {"temperature": 0.8, "num_predict": 100}
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            resposta = response.json().get("message", {}).get("content", "Erro interno.").strip()
            self.memoria.append({"role": "assistant", "content": resposta})
            return resposta
        except Exception as e:
            return "Erro de ligação. O meu núcleo neural (Ollama) está offline."

    def ouvir(self):
        with sr.Microphone() as source:
            self.log_callback("\n[Sistema] A ajustar ruído ambiente... Fala agora.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                texto = self.recognizer.recognize_google(audio, language='pt-BR')
                return texto.lower()
            except:
                return None

# ===================================
# CLASSE DA INTERFACE GRÁFICA (O Corpo)
# ===================================
class UltronApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela
        self.title("Ultron AI - Terminal Central")
        self.geometry("700x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Layout Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Caixa de Texto (Histórico de Chat)
        self.chat_box = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="word", state="disabled")
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="nsew")

        # Campo de Entrada de Texto
        self.entrada_texto = ctk.CTkEntry(self, placeholder_text="Escreve o teu comando humano...", font=("Consolas", 14))
        self.entrada_texto.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="ew", ipady=8)
        self.entrada_texto.bind("<Return>", lambda event: self.enviar_comando_texto())

        # Frame para Botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=1, column=1, padx=(0, 20), pady=(0, 20), sticky="e")

        # Botão Enviar (Texto)
        self.btn_enviar = ctk.CTkButton(self.frame_botoes, text="Enviar", width=80, command=self.enviar_comando_texto)
        self.btn_enviar.pack(side="left", padx=5)

        # Botão Microfone (Voz)
        self.btn_mic = ctk.CTkButton(self.frame_botoes, text="🎤 Ouvir", width=80, fg_color="#8B0000", hover_color="#5C0000", command=self.enviar_comando_voz)
        self.btn_mic.pack(side="left", padx=5)

        # Inicializa o Motor IA
        self.escrever_chat("Sistema", "A iniciar protocolos do Ultron... Conectando à RTX.")
        self.ai_engine = UltronEngine(log_callback=self.escrever_chat_simples)
        self.escrever_chat("Ultron", "Sistemas online. O que queres, humano?")

    def escrever_chat(self, remetente, mensagem):
        """Escreve uma mensagem formatada no ecrã."""
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"[{remetente}]: {mensagem}\n\n")
        self.chat_box.see("end") # Faz scroll automático para o fundo
        self.chat_box.configure(state="disabled")

    def escrever_chat_simples(self, mensagem):
        """Escreve avisos do sistema sem nome de remetente."""
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{mensagem}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def desativar_interface(self):
        self.btn_enviar.configure(state="disabled")
        self.btn_mic.configure(state="disabled")
        self.entrada_texto.configure(state="disabled")

    def ativar_interface(self):
        self.btn_enviar.configure(state="normal")
        self.btn_mic.configure(state="normal")
        self.entrada_texto.configure(state="normal")
        self.entrada_texto.focus()

    # ===================================
    # PROCESSAMENTO EM SEGUNDO PLANO (THREADS)
    # ===================================
    def enviar_comando_texto(self):
        texto = self.entrada_texto.get().strip()
        if not texto: return

        self.entrada_texto.delete(0, "end")
        self.escrever_chat("Tu", texto)
        
        # Inicia uma thread para a IA não bloquear o ecrã
        threading.Thread(target=self.processar_ia, args=(texto, False), daemon=True).start()

    def enviar_comando_voz(self):
        # Inicia uma thread para gravar e processar voz
        threading.Thread(target=self.processar_voz, daemon=True).start()

    def processar_voz(self):
        self.desativar_interface()
        texto_ouvido = self.ai_engine.ouvir()
        
        if texto_ouvido:
            self.escrever_chat("Tu (Voz)", texto_ouvido)
            self.processar_ia(texto_ouvido, ler_em_voz_alta=True)
        else:
            self.escrever_chat_simples("[Sistema] Não consegui compreender. Tenta novamente.")
            self.ativar_interface()

    def processar_ia(self, prompt, ler_em_voz_alta=False):
        self.desativar_interface()
        self.escrever_chat_simples("A processar...")

        resposta = self.ai_engine.pensar(prompt)
        self.escrever_chat(ASSISTANT_NAME, resposta)

        if ler_em_voz_alta:
            self.ai_engine.falar(resposta)

        self.ativar_interface()

# ===================================
# ARRANQUE DA APLICAÇÃO
# ===================================
if __name__ == "__main__":
    app = UltronApp()
    app.mainloop()