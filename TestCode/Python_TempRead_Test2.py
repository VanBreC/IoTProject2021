from sense_hat import SenseHat
sense = SenseHat()
import paho.mqtt.client as mqtt
import time as time
sense.clear()
broker_address="192.168.1.32"

print("Connecting to MQTT")
client = mqtt.Client("DWF")
client.connect(broker_address)

while True:
    
    temp = sense.get_temperature()
    temp = round(temp,1)
    
    print(temp, "C")
    
    sense.show_message(str(temp))
    
    client.publish("test", temp)
    time.sleep(2)
    
    
