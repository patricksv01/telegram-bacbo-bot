import telebot

bot = telebot.TeleBot("7679563879:AAGsaKb7iufZtuIoUitgnbP_7ccAWiDWA2g")

@bot.message_handler(func=lambda message: True)
def pegar_id(message):
    bot.reply_to(message, f"Chat ID: {message.chat.id}")

bot.polling()