import telebot
from flask import Flask, request

API_TOKEN = '8161236137:AAEhQRE_tXjaRq1JAxO6we3a5uY7qc0T8l4'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return 'Bot está rodando com sucesso!'

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot está ativo!\nEnvie uma mensagem no seu canal para descobrir o ID.")

# Captura mensagens em canais e responde com o ID
@bot.channel_post_handler(func=lambda m: True)
def pegar_id_canal(message):
    canal_id = message.chat.id
    bot.send_message(canal_id, f"🆔 ID do canal: `{canal_id}`", parse_mode="Markdown")

# Inicia o webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-bacbo-bot.onrender.com/8161236137:AAEhQRE_tXjaRq1JAxO6we3a5uY7qc0T8l4')
    app.run(host='0.0.0.0', port=10000)