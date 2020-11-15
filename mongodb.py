from pymongo import MongoClient

client = MongoClient("192.168.0.55:27017")
db = client.bot


def store_chat(chat, email, courses):
    courses_array = []

    for course in courses:
        courses_array.append({
            "id": course["id"],
            "shortname": course["shortname"],
            "fullname": course["fullname"]
        })

    return db.chats.insert_one({
        "id": str(chat.id),
        "type": chat.type,
        "email": email,
        "courses": courses_array,
        "notifications": "1 vez por dia"
    })


def delete_chat(chat):
    return db.chats.delete_one({"id": str(chat.id)})


def get_chat(chat):
    return db.chats.find_one({"id": str(chat.id)})
