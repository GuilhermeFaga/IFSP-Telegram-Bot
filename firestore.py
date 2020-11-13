from google.cloud import firestore

fs = firestore.Client()


def store_chat(chat, email, courses):
    doc = fs.document("chats", str(chat.id))

    courses_array = []

    for course in courses:
        courses_array.append({
            "id": course["id"],
            "shortname": course["shortname"],
            "fullname": course["fullname"]
        })

    return doc.set({
        "type": chat.type,
        "email": email,
        "courses": courses_array,
        "notifications": "1 vez por dia"
    })


def delete_chat(chat):
    doc = fs.document("chats", str(chat.id))
    return doc.delete()


def get_chat(chat):
    doc = fs.document("chats", str(chat.id))
    snapshot = doc.get()
    if not snapshot.exists:
        return False
    return snapshot.to_dict()


doc = fs.document("teste", "123")
doc.set({"teste": 123})
