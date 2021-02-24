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
    temp = temp*(9/5)+32
    temp = round(temp,1)
    
    #print(temp)
    
    sense.show_message(str(temp)+ "F")
    
    client.publish("test", temp)
    time.sleep(2)
    
    
