import telebot
from telebot import types
from flask import Flask
from threading import Thread


app = Flask('')
@app.route('/')
def home(): return "OK"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()


TOKEN = '8225110405:AAG6ISvSX4KNxzyLdV4DCXizBWDLRpOEmVU'
TARGET_CHAT_ID = -1003796818229 
ADMIN_CHAT_ID = 5110146436
TOPIC_ID = 3821
GROUP_LINK = "https://t.me/shlakoCHAT"

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    try:
        m = bot.get_chat_member(TARGET_CHAT_ID, user_id)
        return m.status in ['member', 'administrator', 'creator', 'restricted']
    except Exception as e:
        print(f"Ошибка проверки: {e}")
        return False

@bot.message_handler(commands=['id'])
def send_id(message):
    bot.reply_to(message, f"ID чата: {message.chat.id}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот для ШЛАКО ЧАТА.\nЧтобы отправить донос, вы должны быть в группе.")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ Доступ открыт. Теперь присылайте ваш донос.")
    else:
        bot.answer_callback_query(call.id, "❌ Вы все еще не вступили!", show_alert=True)

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_msg(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Вступить", url=GROUP_LINK))
        markup.add(types.InlineKeyboardButton("✅ Я вступил(а)", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ Вы не в группе!", reply_markup=markup)
        return
    
    if message.text:
        try:
            bot.send_message(TARGET_CHAT_ID, message.text, message_thread_id=TOPIC_ID)
            bot.send_message(ADMIN_CHAT_ID, f"Log: {message.from_user.id} | @{message.from_user.username}")
            bot.send_message(message.chat.id, "✅ Доставлено.")
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Ошибка. Проверьте права бота в группе.")
            print(e)

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True, allowed_updates=["message", "callback_query"])
