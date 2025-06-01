import telebot
from flask import Flask, request

API_TOKEN = '8161236137:AAEhQRE_tXjaRq1JAxO6we3a5uY7qc0T8l4'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Rota principal só para teste
@app.route('/')
def index():
    return '✅ Bot está rodando com sucesso!'

# Rota do Webhook (deve ser /webhook)
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Invalid content type', 403

# Comando /start para testar o bot no privado
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Bot ativo!\nEnvie uma mensagem no seu canal e veja se ele responde com o ID!")

# Captura mensagem enviada no canal e responde com o ID
@bot.channel_post_handler(func=lambda m: True)
def canal_id(message):
    canal_id = message.chat.id
    bot.send_message(canal_id, f"🆔 ID do canal: `{canal_id}`", parse_mode="Markdown")

# Iniciar o Webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-bacbo-bot.onrender.com/webhook')
    app.run(host='0.0.0.0', port=10000)