import os

telegram = {
    "token": os.environ.get('BOT_TOKEN'),
    "username": '@' + os.environ.get('BOT_NAME'),
    "feedback_chat_id": os.environ.get('BOT_FEEDBACKID')
}

moodle = {
    "url": os.environ.get('MOODLE_URL'),
    "baseURL": os.environ.get('MOODLE_URL') + "/webservice/rest/server.php?",
    "userToken": "wstoken=" + os.environ.get('MOODLE_TOKEN'),
    "defaultParams": "&moodlewsrestformat=json"
}

texts = {
    "configurar": "🛠 Para configurar o bot use /config",
    "digite_email": "Digite seu e-mail do Moodle:",
    "email_nao_encontrado": """🛑 E-mail nao encontrado, tente novamente

Digite seu e-mail do Moodle:""",
    "email_invalido": """⚠ E-mail invalido, tente novamente

Digite seu e-mail do Moodle:""",
    "logado_sucesso": "✅ Logado com sucesso!",
    "feedback": "💬 Escreva seu feedback:",
    "feedback_enviado": "😊 Obrigado pelo seu feedback!"
}
