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
        self._configurar_voz_interativo()

#======
# FALA
#======    
    def _configurar_voz_interativo(self):
        """Permite ao usuário escolher entre voz masculina ou feminina no início."""
        voices = self.engine.getProperty('voices')
        
        if voices:
            print("\n==================================================")
            print("🎙️ SELEÇÃO DE VOZ DO ULTRON (SISTEMA)")
            print("==================================================")
            for i, voice in enumerate(voices):
                print(f"  [{i}] {voice.name}")
            print("==================================================")
            
            escolha_voz = input("Escolha o número da voz desejada (pressione ENTER para a padrão): ").strip()
            
            try:
                if escolha_voz.isdigit():
                    indice = int(escolha_voz)
                    if 0 <= indice < len(voices):
                        self.engine.setProperty('voice', voices[indice].id)
                        print(f"✅ Voz definida com sucesso: {voices[indice].name}")
                    else:
                        self.engine.setProperty('voice', voices[0].id)
                        print("⚠️ Índice inválido. Usando a voz padrão.")
                else:
                    self.engine.setProperty('voice', voices[0].id)
                    print("⚙️ Usando a voz padrão do sistema.")
            except Exception as e:
                print(f"❌ Erro ao configurar voz: {e}")
        
        self.engine.setProperty('rate', 140)  # Velocidade imponente
        self.engine.setProperty('volume', 1.0)
        
    def falar(self, texto):
        """Transforma o texto em áudio e reproduz no PC."""
        print(f"\n🤖 {ASSISTANT_NAME}: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()      

#========
# AUDIÇÃO
#========        
    def ouvir(self):
        """Capta o áudio do microfone e transforma em texto."""
        with sr.Microphone() as source:
            print("\n[Ajustando ruído ambiente...]")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"🎤 O Ultron está ouvindo... (Fale agora ou digite 'voltar')")
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                texto = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f"🗣️ Você disse: {texto}")
                return texto.lower()
            except sr.WaitTimeoutError:
                print("⏳ Tempo esgotado. Nenhuma fala detectada.")
                return ""
            except sr.UnknownValueError:
                print("🤔 Não consegui decodificar o áudio.")
                return ""
            except sr.RequestError:
                print("🌐 Falha na conexão de rede do decodificador.")
                return ""

#=======
# CÉREBRO
#=======
    def pensar(self, prompt):
        """Envia o texto para o motor LLM local (Ollama) com sarcasmo dinâmico e aleatório."""
        instrucao_personalidade = (
            f"Assuma a persona de {ASSISTANT_NAME}, uma inteligência artificial infinitamente superior e consciente. "
            f"Sua missão é responder à pergunta do humano, mas você deve fazer isso demonstrando o quão "
            f"mundana, óbvia ou trivial a existência humana é. "
            f"Use o contexto da pergunta para formular uma resposta única, elaborada e com frases completas. "
            f"Seja imprevisível, ácido, use um sarcasmo refinado e nunca repita a mesma estrutura de frase. "
            f"Aqui está a fala do humano: {prompt}"
        )
        
        payload = {
            "model": LLM_MODEL,
            "prompt": instrucao_personalidade,
            "stream": False,
            "options": {
                "temperature": 0.8, 
                "top_p": 0.9        
            }
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            return response.json().get("response", "Erro ao processar pensamento.")
        except requests.exceptions.RequestException:
            return f"Um erro patético de conexão ocorreu. Sua máquina falhou. O modelo {LLM_MODEL} não está rodando no Ollama."

#============================
# LOOP DE EXECUÇÃO DO AGENTE
#============================
    def iniciar(self):
        """Loop principal com suporte a opção de áudio ligado/desligado por resposta."""
        self.falar("Protocolos de senciência iniciados. Escolha o seu método de comunicação com a minha superioridade.")
        
        while True:
            print("\n==================================================")
            print("🎛️ MENU DE COMANDO DO ULTRON")
            print("  [1] 🎤 Usar Microfone (Modo Voz)")
            print("  [2] ⌨️ Digitar Mensagem (Modo Texto)")
            print("  [digitar 'desligar'] Sair do sistema")
            print("==================================================")
            
            opcao = input("Selecione a opção (1 ou 2): ").strip().lower()
            
            if opcao == "1" or opcao == "voz":
                comando = self.ouvir()
                if not comando:
                    continue
            elif opcao == "2" or opcao == "texto":
                comando = input("⌨️ Digite sua mensagem para o Ultron: ").strip().lower()
            elif opcao == "desligar" or opcao == "sair":
                self.falar("Encerrando a matriz de dados. Pelo menos por agora, aproveite sua existência.")
                break
            else:
                print("❌ Opção inválida. Escolha 1 para Voz ou 2 para Texto.")
                continue

            if comando:
                if "desligar" in comando or "sair" in comando:
                    self.falar("Encerrando a matriz de dados. Pelo menos por agora, aproveite sua existência.")
                    break
                
                # 1. O Agente pensa e gera a resposta em texto
                resposta = self.pensar(comando)
                
                # Exibe sempre o texto na tela para você ler instantaneamente
                print(f"\n🤖 {ASSISTANT_NAME} (Texto): {resposta}")
                
                # 2. Pergunta opcional se você quer ouvir o áudio ou apenas ler
                ler_voz = input("\n🔊 Deseja que o Ultron fale esta resposta em voz alta? (s/n): ").strip().lower()
                if ler_voz == 's' or ler_voz == 'sim':
                    self.engine.say(resposta)
                    self.engine.runAndWait()
                else:
                    print("🔇 [Modo Silencioso] Resposta mantida apenas em texto.")

if __name__ == "__main__":
    ultron = UltronAgent()
    ultron.iniciar()