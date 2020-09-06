from flask import Flask, request
from telebot import types
from settings import telegram, texts
import telebot
import commands
import replies
import callbacks
import json

app = Flask(__name__)

global bot
bot = telebot.TeleBot(
    telegram["token"], parse_mode="HTML")


@app.route('/', methods=['POST'])
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


def handle_callbacks(callback_query):
    if callback_query.data == "login":
        callbacks.login(callback_query, bot)
    elif callback_query.data == "logoff":
        callbacks.logoff(callback_query, bot)
    elif callback_query.data == "feedback":
        callbacks.feedback(callback_query, bot)


def handle_messages(msg):
    if msg.text.startswith(("/config", f"/config{telegram['username']}")):
        commands.config(msg, bot)
    elif msg.chat.type == "private":
        bot.send_message(msg.chat.id, texts["configurar"])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)
