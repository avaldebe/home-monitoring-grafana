# Home sensor data monitoring with MQTT, InfluxDB and Grafana

Built upon [http://nilhcem.com/iot/home-monitoring-with-mqtt-influxdb-grafana](http://nilhcem.com/iot/home-monitoring-with-mqtt-influxdb-grafana)  

## Local files

- `mosquitto/`: configuration files for mosquitto container
- `Dockerfile`: [PyPMS][] is a python util that
  - reads a PMSx003 sensor and publishes sensor data to MQTT
  - receives MQTT data and persists those to InfluxDB

[pypms]: https://pypi.org/project/pypms/

## Setup

### Mosquitto + InfluxDB + Grafana

Make sure you have `docker` and `docker-compose` installed.  
For the example, a Raspberry Pi 3 B+ with Raspbian will be used.

Set the `DATA_DIR` environment variable to the path where will be stored local data (e.g. in `/tmp`):

```bash
export DATA_DIR=/mnt/aqmon

# create data directories with write access
mkdir -p $DATA_DIR/mosquitto/data $DATA_DIR/mosquitto/log $DATA_DIR/influxdb $DATA_DIR/grafana
sudo chown -R 1883:1883 $DATA_DIR/mosquitto
sudo chown -R 472:472 $DATA_DIR/grafana

# save env values
cat > .env << _EOF
DATA_DIR=$DATA_DIR
MQTT_USER=mqttuser
MQTT_PASS=mqttpassword
DB_USER=root
DB_PASS=root
_EOF

# launch/update containers
docker-compose up -d
```

Mosquitto username and passwords are `mqttuser` and `mqttpassword`.
To change these, see the `Optional: Update mosquitto credentials` section.

## Sensors

Sensors should send data to the mosquitto broker following the
[Homie][] spec: `aqmon/{device_id}/{node_id}/{property}`
For example: `aqmon/livingroom/pm10/concentration`.

[Homie]: https://homieiot.github.io/specification/spec-core-v2_0_0

## Grafana setup

- Access Grafana from `http://<host ip>:3000`
- Log in with user/password `admin/admin`
- Go to Configuration > Data Sources
- Add data source (InfluxDB)
  - Name: `InfluxDB`
  - URL: `http://influxdb:8086`
  - Database: `home_db`
  - User: `root`
  - Password: `root`
  - Save & Test
- Create a Dashboard
  - Add Graph Panel
  - Edit Panel
  - Data Source: InfluxDB
  - FROM: `[default] [pm10] WHERE [location]=[livingroom]`
  - SELECT: `field(value)`
  - FORMAT AS: `Time series`
  - Draw mode: Lines
  - Stacking & Null value: Null value [connected]
  - Left Y
    - Unit: Temperature > Celsius
  - Panel title: Temperature (°C)

## Optional: Update mosquitto credentials

To change default MQTT username and password

```bash
# source old new env values
source .env
# new username/password
MQTT_USER=new_username
MQTT_PASS=new_password

# replace username/password
echo -n "" > ./mosquitto/users
docker run --rm \
  -v ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf \
  -v ./mosquitto/users:/mosquitto/config/users \
  eclipse-mosquitto:1.6.12 \
  mosquitto_passwd -b /mosquitto/config/users $MQTT_USER $MQTT_PASS

# write new env values
cat > .env << _EOF
DATA_DIR=$DATA_DIR
MQTT_USER=$MQTT_USER
MQTT_PASS=$MQTT_PASS
DB_USER=$DB_USER
DB_PASS=$DB_PASS
_EOF

# launch/update containers
docker-compose up -d
```

## Alternative: Using docker manually instead of docker compose

```bash
# source env values
source .env

# mosquitto
docker run -d -p 1883:1883 \
  -v ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf \
  -v ./mosquitto/users:/mosquitto/config/users \
  -v $DATA_DIR/mosquitto/data:/mosquitto/data \
  -v $DATA_DIR/mosquitto/log:/mosquitto/log \
  --name mosquitto eclipse-mosquitto:1.6.12

# influxdb
docker run -d -p 8086:8086 \
  -v $DATA_DIR/influxdb:/var/lib/influxdb \
  --name influxdb influxdb:1.8.3

# grafana
docker run -d -p 3000:3000 \
  -v $DATA_DIR/grafana:/var/lib/grafana \
  --name=grafana grafana/grafana:7.2.2

# PyPMS
docker build -t avaldebe/pypms .

# mqttbridge: pms gets username/password from env vars, i.e. .env
docker run -d --env-file .env --name mqttbridge avaldebe/pypms \
  pms bridge \
    --mqtt-topic "aqmon/+/+/+" --mqtt-host mosquitto \
    --db-host influxdb --db-name home_db

# mqttpypms: pms gets username/password from env vars, i.e. .env
docker run -d --env-file .env --name mqttpypms avaldebe/pypms \
  pms \
    --sensor-model PMSx003 --serial-port /dev/ttyUSB0 --interval 60 \
  mqtt \
    --topic "aqmon/h501-livingroom" --mqtt-host mosquitto
```
