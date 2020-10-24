FROM python:3.7-alpine

LABEL maintainer="avaldebe" \
      description="MQTT to InfluxDB Bridge with PyPMS"

# PyPMS with MQTT support
RUN pip install --no-cache-dir "pypms[mqtt,influxdb]>=0.3.1"

CMD ["pms", "bridge", \
     "--mqtt-topic", "aqmon/+/+/+", \
     "--mqtt-host", "mosquitto", \
     "--mqtt-user", "mqttuser", \
     "--mqtt-pass", "mqttpassword", \
     "--db-host", "influxdb", \
     "--db-user", "root", \
     "--db-pass", "root", \
     "--db-name", "home_db" \
]
