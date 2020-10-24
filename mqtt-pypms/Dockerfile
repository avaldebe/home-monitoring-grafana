FROM python:3.7-alpine

LABEL maintainer="avaldebe" \
      description="PMSx003 to MQTT with PyPMS"

# PyPMS with MQTT support
RUN pip install --no-cache-dir "pypms[mqtt]>=0.3.1"

# sample PMSx003 @ /dev/ttyUSB0 every 60s
CMD ["pms", \
     "--sensor-model", "PMSx003", \
     "--serial-port", "/dev/ttyUSB0", \
     "--interval", "60", \
     "mqtt", \
     "--topic", "aqmon/h501-livingroom", \
     "--mqtt-host", "mosquitto", \
     "--mqtt-user", "mqttuser", \
     "--mqtt-pass", "mqttpassword" \
]
