import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Configurações do WhatsApp
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0/577247788797672/messages"  # ID do número de telefone correto
WHATSAPP_TOKEN = "EAAIk4wzgVRsBO6wkxWn8g7xjZBWbKdNuYQrI77TLQJ1tsxBD9OP5Te9zZBtfzqaGCSEv8bbjKjEJgoTigFMhmjhiGZBZBwX67YZCRPaLzsMjPRZCBoACqcih8SPQ84jQ25MDKPM3L0Lpkr7wqL1r6LpoaWEnzD3Q5t7SZCZClZCNhZBRraMLzUjLvQkNrZBEoI3aUf6dG0l9YhKoeJwNGDDMZCXJaYtxV2RfVgZBfKnVk3jGDfGUZD"

# Configuração do GPT Personalizado
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_API_KEY = "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"

@app.route("/")
def index():
    return "Bot está funcionando!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        # Extrair mensagem do WhatsApp
        user_message = data['messages'][0]['text']['body']
        sender = data['messages'][0]['from']

        # Enviar mensagem ao GPT personalizado
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GPT_API_KEY}"
        }
        payload = {
            "model": "gpt-4",  # Certifique-se de usar o modelo configurado no GPT
            "messages": [{"role": "user", "content": user_message}],
        }
        response = requests.post(GPT_API_URL, headers=headers, json=payload)
        gpt_reply = response.json()['choices'][0]['message']['content']

        # Responder no WhatsApp
        whatsapp_payload = {
            "messaging_product": "whatsapp",
            "to": sender,
            "text": {"body": gpt_reply}
        }
        whatsapp_headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        requests.post(WHATSAPP_API_URL, json=whatsapp_payload, headers=whatsapp_headers)

    except Exception as e:
        print(f"Erro: {e}")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Porta esperada pelo Railway
    app.run(host="0.0.0.0", port=port)
