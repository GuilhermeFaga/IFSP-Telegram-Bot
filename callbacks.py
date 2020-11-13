from telebot import types
from settings import texts, moodle
import mongodb


def login(callback_query, bot):
    bot.send_message(callback_query.message.chat.id, texts["digite_email"],
                     reply_markup=types.ForceReply())


def logoff(callback_query, bot):
    msg = callback_query.message
    mongodb.delete_chat(msg.chat)

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Logar", callback_data="login"),
               types.InlineKeyboardButton("Moodle", url=moodle["url"]))

    message = f"""Chat info

<b>Login:</b> 🚫
<b>Cursos:</b> 🚫
<b>Notificacoes:</b> 🚫"""

    bot.edit_message_text(message, chat_id=msg.chat.id,
                          message_id=msg.message_id, reply_markup=markup)


def feedback(callback_query, bot):
    bot.send_message(callback_query.message.chat.id, texts["feedback"],
                     reply_markup=types.ForceReply())


def show_courses(callback_query, bot):
    pass
