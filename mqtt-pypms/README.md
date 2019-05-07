# PMSx003 to MQTT with PySerial

## Build

```bash
docker build -t avaldebe/mqttpypms .
```


## Run

```bash
docker run -d --name mqttpypms avaldebe/mqttpypms
```


## Dev

```bash
docker run -it --rm -v $PWD:/app --name python python:3.7-alpine sh
```
