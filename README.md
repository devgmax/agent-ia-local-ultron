# 🤖 Projeto Ultron: Agente IA Local (Open-Source)

---

## 🇧🇷 Português

Este é um projeto de código aberto para criar o seu próprio Agente de Inteligência Artificial 100% local, focado em privacidade e performance bruta. Ele ouve comandos pelo microfone, processa o pensamento usando modelos LLM robustos via **Ollama**, e responde com voz através do seu computador.

O agente possui uma instrução de sistema (System Prompt) customizável, atualmente configurada para responder com o sarcasmo e a acidez de uma verdadeira inteligência artificial superior.

### ⚙️ Como Instalar e Rodar

**1. Instale o motor de IA (Ollama)**
* Baixe e instale o Ollama.
* No terminal, baixe o modelo de inteligência desejado rodando: `ollama run llama3`

**2. Clone o repositório e prepare o ambiente**
* Ative o ambiente virtual no Windows rodando `venv\Scripts\activate` ou no Mac/Linux rodando `source venv/bin/activate`.

**3. Instale as dependências de Áudio e Python**
* Execute a instalação: `pip install pyttsx3 speechrecognition pyaudio requests`
* Nota: No Windows, se o `pyaudio` falhar, você pode precisar instalar o pacote `pipwin` e depois rodar `pipwin install pyaudio`.

**4. Customize seu Assistente**
* Abra o arquivo `agente_local.py` e altere a variável global no topo do arquivo para mudar o nome do bot, e edite o método `pensar()` para alterar a personalidade dele.

**5. Rode o Agente!**
* Inicie o robô com o comando `python agente_local.py`

---

## 🇺🇸 English

This is an open-source project to create your own 100% local, privacy-focused Artificial Intelligence Agent. It listens to microphone commands, processes thoughts using robust LLMs via **Ollama**, and responds with voice through your computer.

The agent features a customizable System Prompt, currently configured to respond with the sarcasm and acidity of a true superior artificial intelligence.

### ⚙️ How to Install and Run

**1. Install the AI Engine (Ollama)**
* Download and install Ollama.
* In your terminal, download your preferred AI model by running: `ollama run llama3`

**2. Clone the repository and setup the environment**
* Activate the virtual environment on Windows using `venv\Scripts\activate` or on Mac/Linux using `source venv/bin/activate`.

**3. Install Audio and Python dependencies**
* Run the installation: `pip install pyttsx3 speechrecognition pyaudio requests`
* Note: On Windows, if `pyaudio` fails, you may need to install the `pipwin` package and then run `pipwin install pyaudio`.

**4. Customize your Assistant**
* Open the `agente_local.py` file to change the global name variable, and edit the `pensar()` method to tweak the agent's core personality.

**5. Run the Agent!**
* Start the robot by running `python agente_local.py`
