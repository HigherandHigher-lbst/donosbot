import telebot

TOKEN = '8225110405:AAFJd_G3lAR4j8rDvhGciIwCVBW6AwCrfws'
TARGET_CHAT_ID = -1003796818229  
ADMIN_CHAT_ID = 5110146436        
TOPIC_ID = 3021                   

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветик! Хочешь написать донос? Пиши сюда ниже👇")

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_message(message):
    if message.text:
        
        bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=message.text,
            reply_to_message_id=TOPIC_ID
        )
    
    
    username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
    info = f"Донесено от:\nID: {message.from_user.id}\nUsername: {username}"
    bot.send_message(ADMIN_CHAT_ID, info)
    
    bot.send_message(message.chat.id, "Донос успешно отправлен✅")

bot.polling(none_stop=True)   
