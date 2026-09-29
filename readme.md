# Multi-Model Chat with Ollama + ngrok

A small proof-of-concept that connects **multiple Ollama models into one continuous conversation**.

The text model runs locally on your PC, while the vision-language model runs remotely on **Kaggle** and is exposed through **ngrok**.

The application automatically switches models based on whether the user sends a normal text query or an image attachment.

## What it does

* 💬 Text queries → local `qwen3:1.7b`
* 🖼️ Image queries → remote `qwen3-vl:2b`
* 🔄 Maintains one continuous `chat_history`
* ⚡ Streams responses from both models
* 🌐 Remote Ollama server exposed using ngrok
* 🐍 Built with Python + Ollama

### Architecture

```text
                    Your conversation
                           │
                           ▼
                    Python application
                           │
              ┌────────────┴────────────┐
              │                         │
         Text query               Image query
              │                         │
              ▼                         ▼
       Local Ollama               ngrok tunnel
       qwen3:1.7b                     │
                                      ▼
                               Kaggle Ollama
                               qwen3-vl:2b
```

The important part is that the **conversation history stays in the Python application**, even when the model handling the request changes.

---

## Requirements

* Python 3.x
* [Ollama](https://ollama.com/) installed locally
* A Kaggle account
* An ngrok account
* An ngrok authentication token

---

## 1. Setup the local PC

Install Ollama and pull the text model:

```bash
ollama pull qwen3:1.7b
```

Start Ollama:

```bash
ollama serve
```

Ollama normally exposes its API at:

```text
http://localhost:11434
```

Install the Python dependencies:

```bash
pip install ollama python-dotenv
```

---

## 2. Setup the Kaggle server

Create a Kaggle Notebook and run:

```bash
sudo apt-get install zstd
curl -fsSL https://ollama.com/install.sh | sh
pip install pyngrok ollama
```

Start Ollama:

```python
import subprocess

subprocess.Popen(["ollama", "serve"])
```

Ollama will listen on:

```text
localhost:11434
```

---

## 3. Create the ngrok tunnel

Add your ngrok authentication token to **Kaggle Secrets** with the name:

```text
NGROK_AUTHTOKEN
```

Then:

```python
from pyngrok import ngrok
from kaggle_secrets import UserSecretsClient

secrets = UserSecretsClient()

ngrok.set_auth_token(
    secrets.get_secret("NGROK_AUTHTOKEN")
)

tunnel = ngrok.connect(
    "11434",
    host_header="localhost:11434"
)

print(tunnel.public_url)
```

Copy the generated public URL.

---

## 4. Configure the local application

Create a `.env` file:

```env
NGROK_TUNNEL_PUBLIC_URL=https://your-ngrok-url.ngrok-free.app
```

The Python application uses this URL to create an Ollama client for the remote VLM:

```python
client = Client(host=tunnel_url)
```

---

## 5. Run the application

Make sure your **local Ollama server is running**, then:

```bash
python llamacorn.py
```

Normal messages use the local text model:

```text
>>> Tell me a short story
```

To send an image:

```text
>>> Can you describe this image? -a
```

The application will ask for the image path/link and route the request to the remote VLM.

Exit with:

```text
/bye
```

---

## Useful Ollama commands

List installed models:

```bash
ollama list
```

Pull a model:

```bash
ollama pull <model-name>
```

Run a model:

```bash
ollama run <model-name>
```

Check the server:

```bash
curl http://localhost:11434/api/tags
```

---

## Tech Stack

**Python · Ollama · Qwen3 · Qwen3-VL · Kaggle · ngrok**

## Status

This is a **proof-of-concept experiment**, not a production-ready deployment.

The goal was to explore how different models can be used as different capabilities while maintaining a single conversational history.

## Screenshots

See the `/screenshots` folder for examples of:

* Local text-model execution
* Remote VLM execution
* Ollama running on Kaggle
* Requests reaching the remote server
