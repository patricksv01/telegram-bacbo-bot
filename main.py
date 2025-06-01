import telebot

bot = telebot.TeleBot("8161236137:AAEhQRE_tXjaRq1JAxO6we3a5uY7qc0T8l4")

@bot.message_handler(func=lambda message: True)
def pegar_id(message):
    bot.reply_to(message, f"Chat ID: {message.chat.id}")

bot.polling()