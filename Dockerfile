FROM arm64v8/python:3.9.0-buster

COPY qemu-arm-static /usr/bin

WORKDIR /code

COPY requirements.txt ./

RUN apt-get update

RUN apt-get install build-essential

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8090

EXPOSE 8090

CMD ["python3","./main.py"]