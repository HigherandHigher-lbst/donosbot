import telebot
from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
    return "Бот жив!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = '8225110405:AAFwYRq9eeviM-mZZiJIk7mvnCV66dwKhng'
TARGET_CHAT_ID = -1001796038229
ADMIN_CHAT_ID = 5110146436
TOPIC_ID = 3821

bot = telebot.TeleBot(TOKEN)


def is_user_in_group(user_id):
    try:
        member = bot.get_chat_member(TARGET_CHAT_ID, user_id)
        
        
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка при проверке пользователя {user_id}: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "*** УСЛОВИЯ ИСПОЛЬЗОВАНИЯ БОТА ДОНОСЫ ***\n\n"
        "1. Конфиденциальность: Каждое обращение фиксирует ваш ID. Он доступен администратору...\n"
        "2. Целевое использование: Сообщения не должны быть спамом или флудом.\n"
        "3. Наказания: Бан за ложные доносы или нарушения.\n"
        "ВАЖНО: Пользуясь ботом, вы соглашаетесь с правилами."
    )
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "*** Пиши донос после этого сообщения! ***")

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_message(message):
    
    if not is_user_in_group(message.from_user.id):
        bot.send_message(
            message.chat.id, 
            "❌ **Доступ ограничен!**\n\nЧтобы отправлять доносы, вы должны быть участником нашей группы. Пожалуйста, вступите в неё и попробуйте снова."
        )
        return

    
    if message.text:
        try:
            
            bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=message.text,
                message_thread_id=TOPIC_ID 
            )

            
            username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
            info = f"🔔 **Донос от:**\nID: `{message.from_user.id}`\nUsername: {username}"
            
            
            bot.send_message(ADMIN_CHAT_ID, info, parse_mode="Markdown")

            
            bot.send_message(message.chat.id, "✅ Донос успешно отправлен 🕊️")
            
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Произошла ошибка при отправке. Попробуйте позже.")
            print(f"Ошибка отправки: {e}")

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен...")
    bot.polling(none_stop=True)

