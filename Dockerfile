FROM arm64v8/python:3.9.0-buster

COPY qemu-arm-static /usr/bin

WORKDIR /

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8090

EXPOSE 8090

CMD ["python3","./main.py"]