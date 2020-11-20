from settings import telegram, texts
import telebot
import commands
import replies
import callbacks


global bot
bot = telebot.TeleBot(
    telegram["token"], parse_mode="HTML")


@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    if msg.reply_to_message:
        handle_replies(msg)
    elif not msg.from_user.is_bot and not msg.group_chat_created:
        handle_messages(msg)


def handle_replies(msg):
    if texts["digite_email"] in msg.reply_to_message.text:
        replies.login(msg, bot)
    elif texts["feedback"] in msg.reply_to_message.text:
        replies.feedback(msg, bot)


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "login":
        callbacks.login(call, bot)
    elif call.data == "logoff":
        callbacks.logoff(call, bot)
    elif call.data == "feedback":
        callbacks.feedback(call, bot)
    elif call.data == "ver_cursos":
        callbacks.courses(call, bot)
    elif call.data == "config":
        commands.config(callback_query=call, bot=bot, msg=None)
    elif call.data == "calendar":
        callbacks.calendar(call, bot)


def handle_messages(msg):
    if msg.text.startswith(("/config", f"/config{telegram['username']}")):
        commands.config(msg, bot)
    elif msg.chat.type == "private":
        bot.send_message(msg.chat.id, texts["configurar"])


print("Bot started")
bot.polling()
