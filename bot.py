import telebot

TOKEN = '8225110405:AAE6PO-F3GVDxRzbd2LJqUTBLaxcpLY2BXw'
TARGET_CHAT_ID = -1003796818229  
ADMIN_CHAT_ID = 5110146436         

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветик! Хочешь написать донос? Пиши ниже👇(за фейк будет варн!).")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    
    bot.send_message(TARGET_CHAT_ID, message.text)
    
    
    info = f"Донесено от:\nID: {message.from_user.id}\nUsername: @{message.from_user.username}"
    bot.send_message(ADMIN_CHAT_ID, info)

    
    bot.send_message(message.chat.id, "✅ Отправлено.")

bot.polling()
