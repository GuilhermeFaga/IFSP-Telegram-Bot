from time import time
from telebot import types
from settings import texts, moodle
import moodleAPI
import mongodb
import re
import time
import calendar as cal
from datetime import datetime
from dateutil.relativedelta import relativedelta


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


def courses(callback_query, bot):
    msg = callback_query.message
    user_email = mongodb.get_chat(callback_query.message.chat)["email"]
    courses = moodleAPI.get_courses_by_user_email(user_email)
    courses_name = []
    regex = "\((.*)\)"

    markup = types.InlineKeyboardMarkup()
    # markup_courses = [[]]
    # i = 0

    for course in courses:
        course_id = re.findall(regex, course['idnumber'])
        course_id = course_id[0] if course_id else "None"
        # if course_id != "None":
        #     markup_courses[i].append(types.InlineKeyboardButton(
        #         course_id, callback_data=f"course/{course['idnumber']}"))
        #     if len(markup_courses[i]) >= 3:
        #         markup_courses.append([])
        #         i += 1
        courses_name.append(f"{course_id}: {course['displayname']}")
        courses_name.append("----------")

    # for markup_course in markup_courses:
    #     markup.add(*markup_course)

    markup.add(types.InlineKeyboardButton("« Voltar", callback_data="config"))
    nl = '\n'
    message = f"""<b>Seus cursos</b>
<code>
{nl.join(courses_name)}
</code>
"""
    bot.edit_message_text(message, chat_id=msg.chat.id,
                          message_id=msg.message_id, reply_markup=markup)


def calendar(callback_query, bot):
    msg = callback_query.message
    user_email = mongodb.get_chat(callback_query.message.chat)["email"]
    courses = moodleAPI.get_courses_by_user_email(user_email)
    events = moodleAPI.get_courses_events(courses)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("« Voltar", callback_data="config"))

    today = datetime.now()
    today = datetime(year=today.year, month=today.month,
                     day=today.day, hour=0, second=0)

    next_month = today + relativedelta(months=1)

    this_month_calendar = cal.TextCalendar().formatmonth(today.year, today.month)
    this_month_calendar = replace_helper(this_month_calendar, today.day, "▓▓")

    next_month_calendar = cal.TextCalendar().formatmonth(
        next_month.year, next_month.month)

    events_legend = ""
    if events["events"]:
        events["events"].append(
            {"name": "Hoje", "timestart": time.mktime(today.timetuple())})
        events["events"].sort(key=lambda elem: elem["timestart"])
        for event in events["events"]:
            event_date = datetime.fromtimestamp(event["timestart"])
            if event["name"] == "Hoje":
                nl = "\n"
                events_legend += f"▓▓ {event_date.day}/{event_date.month} - {event['name']}{nl}"
            else:
                if event_date.month == today.month:
                    this_month_calendar = replace_helper(
                        this_month_calendar, event_date.day, "░░")
                else:
                    next_month_calendar = replace_helper(
                        next_month_calendar, event_date.day, "░░")
                nl = "\n"
                events_legend += f"░░ {event_date.day}/{event_date.month} - {event['name']}{nl}"

    message = f"""<code>{this_month_calendar}</code>
<code>{next_month_calendar}
{events_legend}
</code>
"""

    bot.edit_message_text(message, chat_id=msg.chat.id,
                          message_id=msg.message_id, reply_markup=markup)


def replace_helper(cal, day, replacement):
    year = re.findall(r"\d{4}", cal)[0]
    cal = re.sub(r"\d{4}", "----", cal)
    pattern = f"\s?({day})\s?" if len(str(day)) == 2 else f"(\s?{day})\s"
    brp = "\n" if re.search("\W" + str(day) + "\n", cal) else ""
    br = "\n" if re.search("\n" + str(day) + "\W", cal) else ""
    s = " " if len(str(day)) == 2 else ""
    sp = " " if len(str(day)) == 2 else " "
    return re.sub(pattern, s + br + replacement + sp + brp, cal, 1).replace("----", year)
