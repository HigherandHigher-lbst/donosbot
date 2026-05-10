import telebot

TOKEN = '8225110405:AAGYJ_xFdgSywGJMaUeTjAn_fhAeK6wYQhE'
TARGET_CHAT_ID = -1003796818229 
MESSAGE_THREAD_ID 
ADMIN_CHAT_ID =  5110146436            

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Хочешь написать донос? Пиши его ниже (за фейк донос варн) .")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if message.text:
        
        bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=message.text,
            message_thread_id=MESSAGE_THREAD_ID
        )
    
    
    username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
    info = f"Донесено от:\nID: {message.from_user.id}\nUsername: {username}"
    bot.send_message(ADMIN_CHAT_ID, info)
    
    bot.send_message(message.chat.id, "Донос успешно отправлен!.")

bot.polling(none_stop=True)   
