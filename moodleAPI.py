from requests.api import options
from settings import moodle
import requests
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def moodle_request(func):
    def inner(arg):
        req = func(arg)
        url = moodle["baseURL"] + moodle["userToken"] + \
            "&wsfunction=" + req["func"] + \
            moodle["defaultParams"]
        return requests.post(url=url, data=req["payload"]).json()
    return inner


@moodle_request
def get_users_by_email(email):
    func = "core_user_get_users_by_field"
    payload = {
        "field": "email",
        "values[0]": email
    }
    return {"payload": payload, "func": func}


@moodle_request
def get_courses_by_user_id(userid):
    func = "core_enrol_get_users_courses"
    payload = {
        "userid": userid
    }
    return {"payload": payload, "func": func}


def get_courses_by_user_email(email):
    users = get_users_by_email(email)
    if not users:
        return None
    return get_courses_by_user_id(users[0]["id"])


@moodle_request
def get_courses_events(courses):
    func = "core_calendar_get_calendar_events"
    courses_id = {}
    for course in courses:
        courses_id[f"events[courseids][{len(courses_id)}]"] = course["id"]

    today = datetime.now()

    this_month_start = datetime(year=today.year, month=today.month,
                                day=1, hour=0, second=0)

    next_month_end = this_month_start + relativedelta(months=2)

    this_month_start_unix = time.mktime(this_month_start.timetuple())
    next_month_end_unix = time.mktime(next_month_end.timetuple())

    payload = {
        "options[userevents]": 0,
        "options[timestart]": int(this_month_start_unix),
        "options[timeend]": int(next_month_end_unix)
    }
    return {"payload": {**courses_id, **payload}, "func": func}


# courses = get_courses_by_user_email("f.galletti@aluno.ifsp.edu.br")

# courses_name = []
# for course in courses:
#     courses_name.append(course["displayname"])

# nl = '\n'
# message = f"""Cursos:

# {nl.join(courses_name)}

# a
# """

# print(message)

# print(courses)
# print(get_courses_events(courses))

# print(int(time.time()))
