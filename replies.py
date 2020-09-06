from telebot import types
from settings import texts, telegram
import firestore
import commands
import test
import moodleAPI


def login(msg, bot):
    if '.' and '@' in msg.text:
        courses = moodleAPI.get_courses_by_user_email(msg.text)
        # courses = test.courses
        if not courses:
            bot.reply_to(msg, texts["email_nao_encotrado"],
                         reply_markup=types.ForceReply())
        else:
            firestore.store_chat(msg.chat, msg.text, courses)
            bot.reply_to(msg, texts["logado_sucesso"])
            commands.config(msg, bot)
    else:
        bot.reply_to(msg, texts["email_invalido"],
                     reply_markup=types.ForceReply())


def feedback(msg, bot):
    bot.reply_to(msg, texts["feedback_enviado"])
    bot.send_message(telegram["feedback_chat_id"], msg.text)
