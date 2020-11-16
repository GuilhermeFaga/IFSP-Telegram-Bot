from telebot import types
from settings import telegram, texts
import telebot
import commands
import replies
import callbacks
import json
import os


global bot
bot = telebot.TeleBot(
    telegram["token"], parse_mode="HTML")


@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    if msg.reply_to_message:
        handle_replies(msg)
    elif not msg.from_user.is_bot and not msg.group_chat_created:
        handle_messages(msg)


def handle_request():
    update = types.Update.de_json(request.json)
    if update.callback_query:
        # bot.send_message(update.callback_query.message.chat.id,
        #                  f"<pre>{json.dumps(request.json)}</pre>")
        handle_callbacks(update.callback_query)
    elif update.message:
        # bot.send_message(update.message.chat.id,
        #                  f"<pre>{json.dumps(request.json)}</pre>")
        msg = update.message
        print(type(msg.chat.id))
        if msg.reply_to_message:
            handle_replies(msg)
        elif not msg.from_user.is_bot and not msg.group_chat_created:
            handle_messages(msg)

    return "OK", 200


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
        callbacks.show_courses(call, bot)


def handle_messages(msg):
    if msg.text.startswith(("/config", f"/config{telegram['username']}")):
        commands.config(msg, bot)
    elif msg.chat.type == "private":
        bot.send_message(msg.chat.id, texts["configurar"])


bot.polling()
