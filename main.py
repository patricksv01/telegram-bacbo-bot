import os
import telebot
from flask import Flask, request
import requests

API_TOKEN = '7687142195:AAH5z5XqJfj7qZn3ZJLyD_QR4aEGKM8POjg'
WEBHOOK_URL = 'https://telegram-bacbo-bot.onrender.com/webhook'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Rota principal para checar se o bot está rodando
@app.route('/')
def index():
    return '🤖 Bot rodando!'

# Rota para receber atualizações via webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Comando /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Olá! 👋 Bot está funcionando corretamente.")

# Comando /check para testar conexões e permissões
@bot.message_handler(commands=['check'])
def check_handler(message):
    chat_id = message.chat.id
    responses = []

    # 1. Testar token válido
    try:
        r = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getMe")
        if r.status_code == 200 and r.json().get("ok"):
            responses.append("✅ Token válido")
        else:
            responses.append("❌ Token inválido ou API inacessível")
    except Exception as e:
        responses.append(f"❌ Erro na requisição getMe: {e}")

    # 2. Testar webhook
    try:
        r = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getWebhookInfo")
        if r.status_code == 200 and r.json().get("ok"):
            webhook_url = r.json()["result"].get("url")
            pending_count = r.json()["result"].get("pending_update_count", 0)
            if webhook_url == WEBHOOK_URL:
                responses.append(f"✅ Webhook configurado corretamente: {webhook_url}")
            else:
                responses.append(f"⚠️ Webhook diferente do esperado: {webhook_url}")
            responses.append(f"🔄 Updates pendentes: {pending_count}")
        else:
            responses.append("❌ Não foi possível obter info do webhook")
    except Exception as e:
        responses.append(f"❌ Erro na requisição getWebhookInfo: {e}")

    # 3. Testar permissão para enviar mensagens
    try:
        test_msg = bot.send_message(chat_id, "🧪 Testando permissão para enviar mensagens...")
        bot.delete_message(chat_id, test_msg.message_id)
        responses.append("✅ Permissão para enviar mensagens OK")
    except Exception as e:
        responses.append(f"❌ Sem permissão para enviar mensagens: {e}")

    responses.append("✅ Bot ativo e respondendo comandos")
    bot.send_message(chat_id, "\n".join(responses))

# Comando /enviar: envia mensagem no chat privado com o usuário
@bot.message_handler(commands=['enviar'])
def enviar_para_si_proprio(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, "🚀 Mensagem enviada no seu chat privado com o bot!")
        bot.reply_to(message, "✅ Mensagem enviada com sucesso.")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar mensagem: {e}")

# Captura o chat_id ao encaminhar mensagens (opcional)
@bot.message_handler(func=lambda m: True)
def pegar_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"🆔 Chat ID: `{chat_id}`", parse_mode="Markdown")

# Inicialização do webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))