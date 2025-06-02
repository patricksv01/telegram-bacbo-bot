import telebot
from flask import Flask, request
import requests

API_TOKEN = '7687142195:AAH5z5XqJfj7qZn3ZJLyD_QR4aEGKM8POjg'
WEBHOOK_URL = 'https://telegram-bacbo-bot.onrender.com/webhook'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return 'Bot rodando!'

# Comando /start simples
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Olá! Bot está funcionando.")

# Comando /check para checklist básico
@bot.message_handler(commands=['check'])
def check_handler(message):
    chat_id = message.chat.id
    responses = []

    # 1. Testar token válido (getMe)
    try:
        r = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getMe")
        if r.status_code == 200 and r.json().get("ok"):
            responses.append("✅ Token válido")
        else:
            responses.append("❌ Token inválido ou API inacessível")
    except Exception as e:
        responses.append(f"❌ Erro na requisição getMe: {e}")

    # 2. Testar webhook configurado
    try:
        r = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getWebhookInfo")
        if r.status_code == 200 and r.json().get("ok"):
            webhook_url = r.json()["result"].get("url")
            pending_count = r.json()["result"].get("pending_update_count", 0)
            if webhook_url == WEBHOOK_URL:
                responses.append(f"✅ Webhook configurado: {webhook_url}")
            else:
                responses.append(f"⚠️ Webhook configurado diferente: {webhook_url}")
            responses.append(f"🔄 Updates pendentes: {pending_count}")
        else:
            responses.append("❌ Não foi possível obter info do webhook")
    except Exception as e:
        responses.append(f"❌ Erro na requisição getWebhookInfo: {e}")

    # 3. Testar permissão para enviar mensagem no chat atual
    try:
        test_message = bot.send_message(chat_id, "🧪 Teste de permissão para enviar mensagem")
        bot.delete_message(chat_id, test_message.message_id)  # Apaga o teste
        responses.append("✅ Permissão para enviar mensagens OK")
    except Exception as e:
        responses.append(f"❌ Sem permissão para enviar mensagens: {e}")

    # 4. Testar se o bot está ativo (responder comandos)
    responses.append("✅ Bot ativo e respondendo comandos")

    # Monta e envia resposta
    bot.send_message(chat_id, "\n".join(responses))

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=10000)