import telebot
from telebot import types
from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = '8225110405:AAFwYRq9eeviM-mZZiJIk7mvnCV66dwKhng' 
TARGET_CHAT_ID = -1001796038229
ADMIN_CHAT_ID = 5110146436
TOPIC_ID = 3821
GROUP_LINK = "t.me/shlakoCHAT"

bot = telebot.TeleBot(TOKEN)


RULES_TEXT = (
    "*** условия использования бота доносы ***\n\n"
    "1 Конфиденциальность: Каждое обращение фиксирует ваш технический ID. Он доступен только администратору. "
    "Мы гарантируем, что данные не передаются третьим лицам.\n"
    "2 Целевое использование: Спам и флуд караются.\n"
    "3 Ошибочные доносы: Немедленно сообщите админу, иначе — варн.\n"
    "4 Клевета: Мут или бан без права апелляции.\n\n"
    "ВАЖНО: Используя бота, вы принимаете данные условия."
)


def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(TARGET_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

Е
@bot.chat_member_handler()
def welcome_on_join(chat_member_update):
    if chat_member_update.new_chat_member.status == "member":
        user_id = chat_member_update.new_chat_member.user.id
        try:
            bot.send_message(user_id, "👋 Привет! Ты вступил в группу. Правила бота:\n\n" + RULES_TEXT)
        except Exception:
            pass


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, RULES_TEXT)
    bot.send_message(message.chat.id, "⬇️ **Пиши донос после этого сообщения!**")


@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ Проверка прошла! Присылай сообщение.")
    else:
        bot.answer_callback_query(call.id, "❌ Ты всё еще не в группе!", show_alert=True)


@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_message(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Вступить в группу", url=GROUP_LINK))
        markup.add(types.InlineKeyboardButton("✅ Я вступил(а)", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ Чтобы писать боту, вступи в группу!", reply_markup=markup)
        return

    if message.text:
        try:
            bot.send_message(TARGET_CHAT_ID, message.text, message_thread_id=TOPIC_ID)
            username = f"@{message.from_user.username}" if message.from_user.username else "нет username"
            bot.send_message(ADMIN_CHAT_ID, f"🔔 Донос от: {username}\nID: `{message.from_user.id}`", parse_mode="Markdown")
            bot.send_message(message.chat.id, "✅ Донос отправлен!")
        except Exception:
            bot.send_message(message.chat.id, "❌ Ошибка отправки.")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True, allowed_updates=["message", "callback_query", "chat_member"])
