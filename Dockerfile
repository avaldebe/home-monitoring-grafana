FROM python:3.7-alpine

LABEL maintainer="avaldebe" \
      description="PyPMS: Data acquisition and logging tool for PM sensors with UART interface"

# PyPMS with MQTT and InfluxDB support
RUN pip install --no-cache-dir "pypms[mqtt,influxdb]>=0.3.1"
