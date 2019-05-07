FROM python:3.7-alpine

LABEL maintainer="avaldebe" \
      description="PMSx003 to MQTT with PySerial"

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
