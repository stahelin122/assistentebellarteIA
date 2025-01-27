from flask import Flask, request
import requests

app = Flask(__name__)

# Configurações do WhatsApp
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0/<YOUR_PHONE_NUMBER_ID>/messages"  # Substitua <YOUR_PHONE_NUMBER_ID> pelo ID do seu número
WHATSAPP_TOKEN = "EAAIk4wzgVRsBO0FzYmOpLKxenDXk3q90FlkZAZBZAtgh6p2W2XtoqIknnQvz6U9G3stUKySoZAR64JZAXYh9Bp3xVkSzeM5Uo0Fo2bGE63ZCW8zrc9gfwDtCT3YxPiGee4TZBkUVYowB01kOUGjyvzkfpvXp7QSPNOReZAjfnXRTCopfUyLIzsMS17eSZCqnWVvmARiIs3DeEHBxZB2bBjG2xqfSnmGK5fdEydxfVofQ6mTPYZD"

# Configuração do GPT Personalizado
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_API_KEY = "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"

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
            "model": "gpt-4",  # Certifique-se de usar o modelo correto configurado
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
    app.run(port=5000)
