import telebot
from telebot import types
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Статус: Работает"

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
    "УСЛОВИЯ ИСПОЛЬЗОВАНИЯ БОТА ДОНОСЫ\n\n"
    "Бот функционирует исключительно для ШЛАКО ЧАТА.\n\n"
    "1. Конфиденциальность: Каждое обращение фиксирует ваш технический ID. Он доступен только администратору. "
    "Данные не передаются третьим лицам, за исключением случаев нарушения данных правил.\n\n"
    "2. Целевое использование: Если сообщение не является доносом или нарушает работу бота (спам, флуд), "
    "ваш ID передается персоналу для выдачи наказания:\n"
    "— 1 раз: варн\n"
    "— 2 раз: бан (апелляция через 3 дня).\n\n"
    "3. Ошибочные доносы: Если вы ошиблись, немедленно сообщите админу. В противном случае — варн, повторно — мут на 24 часа.\n\n"
    "4. Клевета и личная неприязнь: Заведомо ложный донос или попытка использовать бота для личной мести карается мутом на 24 часа. "
    "Повторно — бан без права апелляции.\n\n"
    "ВАЖНО: Используя бота, вы автоматически принимаете данные условия и даете согласие на обработку вашего ID в целях модерации.\n\n"
    "Для подтверждения нажмите на реакцию ниже."
)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(TARGET_CHAT_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.chat_member_handler()
def welcome_on_join(chat_member_update):
    if chat_member_update.new_chat_member.status == "member":
        user_id = chat_member_update.new_chat_member.user.id
        try:
            bot.send_message(user_id, RULES_TEXT)
        except:
            pass
@bot.message_handler(commands=['id'])
def get_real_id(message):
     bot.reply_to(message, f"ID этой группы: {message.chat.id}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, RULES_TEXT)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Проверка пройдена. Отправьте сообщение.")
    else:
        bot.answer_callback_query(call.id, "Вы не состоите в группе.", show_alert=True)

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_private_message(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Вступить в группу", url=GROUP_LINK))
        markup.add(types.InlineKeyboardButton("Я вступил(а)", callback_data="check_sub"))
        
        bot.send_message(
            message.chat.id, 
            "Доступ ограничен. Необходимо вступление в группу.",
            reply_markup=markup
        )
        return

    if message.text:
        try:
            bot.send_message(
                chat_id=TARGET_CHAT_ID, 
                text=message.text, 
                message_thread_id=TOPIC_ID
            )
            
            username = f"@{message.from_user.username}" if message.from_user.username else "no_username"
            admin_info = f"Log: New report\nFrom: {username}\nID: {message.from_user.id}"
            bot.send_message(ADMIN_CHAT_ID, admin_info)
            
            bot.send_message(message.chat.id, "Сообщение доставлено.")
        except Exception:
            bot.send_message(message.chat.id, "Ошибка отправки. Бот должен быть администратором группы.")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True, allowed_updates=["message", "callback_query", "chat_member"])
