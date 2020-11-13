from settings import moodle
import requests


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
    # if users['exception']:
    #     print(users)
    #     return None
    return get_courses_by_user_id(users[0]["id"])


print(get_courses_by_user_email("f.galletti@aluno.ifsp.edu.br"))
