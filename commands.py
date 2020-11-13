import mongodb
from telebot import types
from settings import moodle


def config(msg, bot):
    chat = mongodb.get_chat(msg.chat)

    markup = types.InlineKeyboardMarkup(row_width=2)

    if chat:
        markup.add(types.InlineKeyboardButton("Deslogar", callback_data="logoff"),
                   types.InlineKeyboardButton("Moodle", url=moodle["url"]),
                   types.InlineKeyboardButton(
                       "Ver cursos", callback_data="ver_cursos"),
                   types.InlineKeyboardButton(
                       "Editar notificacoes", callback_data="1"),
                   types.InlineKeyboardButton("Enviar feedback", callback_data="feedback"))
    else:
        markup.add(types.InlineKeyboardButton("Logar", callback_data="login"),
                   types.InlineKeyboardButton("Moodle", url=moodle["url"]))

    message = f"""Chat info

<b>Login:</b> {chat["email"] if chat else "🚫"}
<b>Cursos:</b> {len(chat["courses"]) if chat else "🚫"}
<b>Notificacoes:</b> {chat["notifications"] if chat else "🚫"}"""

    bot.send_message(msg.chat.id, message, reply_markup=markup)
