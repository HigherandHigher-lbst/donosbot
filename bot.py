import telebot

TOKEN = '8225110405:AAGfPkDmWwRYHzkA8E9ugG7fOSmDFdEUn_0'
TARGET_CHAT_ID = -1003796818229  
ADMIN_CHAT_ID = 5110146436        

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "ахафщгг51оа1а1115112421412")


@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_message(message):
    if message.text:
        
        bot.send_message(TARGET_CHAT_ID, message.text)
        
        
        username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
        info = f"Донесено от:\nID: {message.from_user.id}\nUsername: {username}"
        bot.send_message(ADMIN_CHAT_ID, info)
    
    
    bot.send_message(message.chat.id, "азфафгрпг1ш51")

bot.polling(none_stop=True)   
