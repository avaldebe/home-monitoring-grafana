#!/usr/bin/env python3

"""
Read PMS5003/PM7003 and push measurements to MQTT server
"""

import paho.mqtt.client as mqtt
import time

from serial import Serial as serial
import struct

MQTT_ADDRESS = 'mosquitto'
MQTT_USER = 'mqttuser'
MQTT_PASSWORD = 'mqttpassword'

MQTT_CLIENT_ID = 'h501-livingroom'
MQTT_TOPIC_PMS = 'aqmon/%s/%%s/concentration'%MQTT_CLIENT_ID
MQTT_TOPIC_STATE = 'aqmon/%s/$online'%MQTT_CLIENT_ID
MQTT_PUBLISH_DELAY = 60

def on_connect(client, userdata, flags, rc):
    client.publish(MQTT_TOPIC_STATE, 'true', 1, True)

def read_pms(device='/dev/ttyUSB0'):
    dev = serial(device, 9600, timeout=0)
    if not dev.isOpen():
        dev.open()
        dev.write(b'\x42\x4D\xE1\x00\x00\x01\x70') # set passive mode
        while dev.in_waiting:
            print(dev.read())

    dev.write(b'\x42\x4D\xE2\x00\x00\x01\x71') # passive mode read
    dev.flush()
    while dev.in_waiting < 32:
        continue

    buffer = dev.read(32)
    #print(buffer)
    assert len(buffer) == 32
    msg = struct.unpack(">HHHHHHHHHHHHHHHH", bytes(buffer))
    assert msg[0] == 0x424D
    assert msg[1] == 28
    assert msg[-1] == sum(buffer[:-2])
    return {'pm01': msg[5], 'pm25': msg[6], 'pm10': msg[7]}

def main():
    mqttc = mqtt.Client(MQTT_CLIENT_ID)
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqttc.will_set(MQTT_TOPIC_STATE, 'false', 1, True)
    mqttc.on_connect = on_connect

    mqttc.connect(MQTT_ADDRESS, 1883, 60)
    mqttc.loop_start()

    last_msg_time = time.time()
    while True:
        try:
            pm = read_pms()   
        except AssertionError:
            pass
        else:
            for k,v in pm.items():
                mqttc.publish(MQTT_TOPIC_PMS%k, v, 1, True)
            last_msg_time = time.time()
        finally:
            delay = MQTT_PUBLISH_DELAY - (time.time() - last_msg_time)
            if delay > 0:
                time.sleep(delay)

if __name__ == '__main__':
    print('PMSx003 to MQTT with PySerial')
    main()
