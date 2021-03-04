###############################
#
# Prior to running this code
# you must install the paho-mqtt
# Python module.
#
# MacOS/Linux:
# pip3 install paho-mqtt
#
# Windows
# pip install paho-mqtt
#
###############################

import paho.mqtt.client as mqtt
import time as time
import random

#declare MQTT variables
#replace this address with the address of your host machine
broker_address="192.168.1.32"

#generate random temperature reading
#seed the generator

#connect to message bus
print("Connecting to MQTT")
client = mqtt.Client("DWF")

client.connect(broker_address)

random.seed(1)
#publish 5 messages to the message queue
#generate random temp ints from 60 to 80
for i in range(5):
    client.publish("testpi3", random.randint(60,80))
    time.sleep(2)

input("Please hit q to quit: ")
