FROM arm64v8/python:3.9.0-buster

COPY qemu-arm-static /usr/bin

RUN pip install pyTelegramBotAPI
RUN pip install pymongo
RUN pip install python-dotenv

COPY . .

CMD ["python3","main.py"]