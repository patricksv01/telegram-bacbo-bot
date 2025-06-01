import telebot
from flask import Flask, request

API_TOKEN = '8161236137:AAEhQRE_tXjaRq1JAxO6we3a5uY7qc0T8l4'
WEBHOOK_URL = 'https://telegram-bacbo-bot.onrender.com/webhook'
SEU_ID_PRIVADO = 5616062392  # Seu ID pessoal para receber o ID do canal

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Endpoint do webhook que o Telegram vai chamar
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

# Página padrão da raiz do site
@app.route('/')
def index():
    return '✅ Bot está rodando com sucesso!'

# Resposta ao comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot está ativo!\nEnvie uma mensagem no seu canal para descobrir o ID.")

# Detecta mensagens enviadas no canal
@bot.channel_post_handler(func=lambda m: True)
def pegar_id_canal(message):
    canal_id = message.chat.id
    nome_canal = message.chat.title
    bot.send_message(SEU_ID_PRIVADO, f"📢 Novo canal detectado!\n\n🆔 ID: `{canal_id}`\n📛 Nome: {nome_canal}", parse_mode="Markdown")

# Inicialização
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=10000)