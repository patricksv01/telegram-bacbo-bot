import telebot

bot = telebot.TeleBot("7648649111:AAGPpFEW9WAT-9I3xXt9jla4kSHCvsUkWZM
")

@bot.message_handler(func=lambda message: True)
def pegar_id(message):
    bot.reply_to(message, f"Chat ID: {message.chat.id}")

bot.polling()