# MQTT to InfluxDB Bridge with PyPMS

```bash
# build
docker build -t avaldebe/mqttbridge .

# run
docker run -d --name mqttbridge avaldebe/mqttbridge

# debug/develop
docker run -it --rm --name python python:3.7-alpine sh
```
