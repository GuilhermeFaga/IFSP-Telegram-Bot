FROM balenalib/raspberry-pi-python

WORKDIR /code

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8090

EXPOSE 8090

CMD ["python3","./main.py"]