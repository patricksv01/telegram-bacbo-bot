import telebot
from flask import Flask, request

API_TOKEN = '8161236137:AAEhQRE_tXjaRq1JAxO6we3a5uY7qc0T8l4'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot com webhook funcionando!")

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot no ar via Render!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://SEU-LINK-DO-RENDER.onrender.com/{API_TOKEN}")
    app.run(host="0.0.0.0", port=10000)