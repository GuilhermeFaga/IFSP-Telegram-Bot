FROM python:3.8.4-slim

WORKDIR /code

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8090

EXPOSE 8090

CMD ["python","./main.py"]