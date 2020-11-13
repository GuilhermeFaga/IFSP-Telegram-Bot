FROM arm64v8/python

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8090

EXPOSE 8090

CMD ["python","main.py"]