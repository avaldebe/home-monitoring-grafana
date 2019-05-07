# MQTT to InfluxDB Bridge

## Build

```bash
docker build -t avaldebe/mqttbridge .
```


## Run

```bash
docker run -d --name mqttbridge avaldebe/mqttbridge
```


## Dev

```bash
docker run -it --rm -v $PWD:/app --name python python:3.7-alpine sh
```
