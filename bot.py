import os
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = "8225110405:AAE6PO-F3GVDxRzbd2LJqUTBLaxcpLY2BXw"
GROUP_ID = -1003796818229 
TOPIC_ID = 11             
ADMIN_ID = 5110146436     

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.chat.type == 'private')
def handle_message(message):
        
    bot.copy_message(
        chat_id=GROUP_ID,	
            
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        message_thread_id=TOPIC_ID
    )
    
    auth_info = f"Автор: {message.from_user.first_name} | ID: {message.from_user.id}"
    bot.send_message(ADMIN_ID, f"Новый донос от {auth_info}")
    
)
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    bot.send_message(message.chat.id, "Отправлено.")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), type('H', (BaseHTTPRequestHandler,), {'do_GET': lambda s: (s.send_response(200), s.end_headers())}))
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
bot.polling(none_stop=True)