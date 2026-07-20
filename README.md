# 🤖 Projeto Ultron: Agente de IA Local

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Llama3-orange.svg)](https://ollama.com/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkblue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

# 🇧🇷 Português (PT-BR)

## Sobre o Projeto

O **Ultron** é um assistente de Inteligência Artificial executado **100% localmente**, sem necessidade de APIs pagas ou envio das conversas para servidores externos.

O projeto reúne em uma única aplicação desktop:

- Interface gráfica moderna
- Modelo de linguagem executado pelo Ollama
- Memória persistente em JSON
- Reconhecimento de voz (Speech-to-Text)
- Síntese de voz (Text-to-Speech)
- Conversação contextual
- Execução multithread para manter a interface sempre responsiva

Toda a inteligência roda diretamente no computador do usuário.

---

# 🚀 Funcionalidades

- Interface moderna utilizando **CustomTkinter**
- Execução totalmente offline
- Conversação contextual
- Memória persistente em JSON
- Aprendizado por comandos de memória
- Entrada por texto
- Entrada por voz
- Resposta por voz
- Processamento em segundo plano utilizando Threads
- Compatível com Windows

---

# 🏗 Arquitetura

| Componente | Tecnologia |
|------------|------------|
| Interface | CustomTkinter |
| IA Local | Ollama |
| Modelo | Llama 3 |
| STT | SpeechRecognition |
| TTS | pyttsx3 |
| Banco de Dados | JSON |
| Comunicação | Requests |
| Concorrência | Threading |

---

# 📋 Requisitos

- Windows 10 ou Windows 11
- Python 3.12 ou superior
- Ollama instalado
- Microfone (opcional)
- Caixa de som (opcional)

---

# ⚙️ Instalação

## 1. Instale o Python

Baixe a versão mais recente do Python:

https://www.python.org/downloads/

Durante a instalação marque:

```
Add Python to PATH
```

Depois confirme:

```powershell
python --version
```

---

## 2. Instale o Ollama

Baixe:

https://ollama.com/download

Após instalar confirme:

```powershell
ollama --version
```

---

## 3. Baixe o modelo Llama 3

Abra um terminal e execute:

```powershell
ollama pull llama3
```

Depois inicie o servidor:

```powershell
ollama serve
```

Deixe essa janela aberta.

---

## 4. Clone o projeto

```powershell
git clone https://github.com/SEU_USUARIO/Ultron.git
```

Entre na pasta:

```powershell
cd Ultron
```

---

## 5. Crie um Ambiente Virtual

```powershell
python -m venv .venv
```

---

## 6. Ative o Ambiente Virtual

Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD

```cmd
.venv\Scripts\activate.bat
```

---

## 7. Atualize o Pip

```powershell
python -m pip install --upgrade pip
```

---

## 8. Instale as Dependências

Caso exista o arquivo requirements.txt:

```powershell
pip install -r requirements.txt
```

Ou instale manualmente:

```powershell
pip install customtkinter
```

```powershell
pip install requests
```

```powershell
pip install speechrecognition
```

```powershell
pip install pyttsx3
```

```powershell
pip install pyaudio
```

---

## 9. Caso o PyAudio apresente erro

Em alguns computadores o PyAudio pode exigir compiladores C++.

Caso isso aconteça utilize um Wheel (.whl) compatível com sua versão do Python ou instale o Build Tools da Microsoft.

---

## 10. Execute a aplicação

```powershell
python ultron_app.py
```

---

# 🧠 Memória Persistente

O Ultron possui memória local utilizando um arquivo JSON.

Sempre que comandos de memória forem detectados, as informações serão armazenadas automaticamente.

Exemplos:

```
Lembre que meu nome é Fulano.
```

```
Memorize que meu projeto utiliza CustomTkinter.
```

```
Guarde que meu computador possui RTX 3060.
```



As informações ficam disponíveis nas próximas conversas.

---

# 📁 Estrutura do Projeto

```
Ultron/

├── ultron_app.py
├── memoria.py
├── memoria_ultron.json
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🔒 Privacidade

Todo o processamento acontece localmente.

Nenhuma conversa é enviada para APIs externas.

A memória é armazenada apenas no computador do usuário.

---

# 🛡 .gitignore Recomendado

```gitignore
# Ambiente Virtual

venv/
.venv/

# Python

__pycache__/
*.pyc

# Banco de Dados

memoria_ultron.json
*.db
*.sqlite3

# Logs

*.log
```

---

# 🇺🇸 English

## About

Ultron is a **100% local AI desktop assistant** powered by Ollama and Llama 3.

Features include:

- Modern desktop interface
- Local LLM inference
- Persistent JSON memory
- Speech Recognition
- Text-to-Speech
- Context-aware conversations
- Background multithreading

Everything runs directly on the user's computer.

---

## Installation

Install Python:

https://www.python.org/downloads/

Install Ollama:

https://ollama.com/download

Download the model:

```bash
ollama pull llama3
```

Start Ollama:

```bash
ollama serve
```

Clone the repository:

```bash
git clone https://github.com/SEU_USUARIO/Ultron.git
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python ultron_app.py
```

---

# 📄 License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

**Developed by Gabriel Max**
