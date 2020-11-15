FROM arm64v8/python:3.9.0-buster


WORKDIR /builder/working/directory
RUN curl -L https://github.com/balena-io/qemu/releases/download/v3.0.0%2Bresin/qemu-3.0.0+resin-arm.tar.gz | tar zxvf - -C . && mv qemu-3.0.0+resin-arm/qemu-arm-static .

COPY --from=builder /builder/working/directory/qemu-arm-static /usr/bin

# COPY qemu-arm-static /usr/bin

RUN pip install pyTelegramBotAPI
RUN pip install pymongo
RUN pip install python-dotenv

COPY . .

CMD ["python3","main.py"]