import telebot
from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
    return "Бот жив!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = '8225110405:AAHx7_ILuEL_G97orY-_e3z_wyl4q-hHgrk'
TARGET_CHAT_ID = -1003796818229
ADMIN_CHAT_ID = 5110146436
TOPIC_ID = 3021

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "УСЛОВИЯ ИСПОЛЬЗОВАНИЯ БОТА ДОНОСЫ
1️ Конфиденциальность: Каждое обращение фиксирует ваш технический ID. Он доступен только администратору. Мы гарантируем, что данные не передаются третьим лицам, за исключением случаев нарушения данных правил.
2️ Целевое использование: Если сообщение не является доносом или нарушает работу бота (спам, флуд), ваш ID передается персоналу для выдачи наказания:
— 1 раз: варн 
— 2 раз: бан  (апелляция через 3 дня).
3️ Ошибочные доносы: Если вы ошиблись, немедленно сообщите админу. В противном случае — варн, повторно — мут на 24 часа.
4️ Клевета и личная неприязнь: Заведомо ложный донос или попытка использовать бота для личной мести карается мутом на 24 часа. Повторно — бан без права апелляции.
ВАЖНО: Используя бота, вы автоматически принимаете данные условия и даете согласие на обработку вашего ID в целях модерации.")
bot.sent_message(message.chat.id, "Пиши донос после этого сообщения!") 

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

        
        bot.send_message(message.chat.id, "Донос успешно отправлен ✅")

if __name__ == "__main__":
    keep_alive() 
    print("Бот запущен...")
    bot.polling(none_stop=True)
