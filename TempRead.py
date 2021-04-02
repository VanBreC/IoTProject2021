from sense_hat import SenseHat
sense = SenseHat()
import paho.mqtt.client as mqtt
from time import sleep
import json
import subprocess
from gpiozero import CPUTemperature
cpu = CPUTemperature()
sense.clear()

broker_address="192.168.1.32"
sship = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")
endofsship = sship.split(".")[3]
client = mqtt.Client("DWF"+endofsship)
try:
    client.connect(broker_address)
except OSError:
    print("Failed to connect to Server | Attempting connection to local VM")
    broker_address="192.168.1.18"
    client.connect(broker_address)
except:
    print("Both Connections Failed")

i = 65
room = ""
AssignRoom = True
TempRead = False



while AssignRoom:
    if i==91:
        i = 48
    elif i==58:
        i = 45
    elif i==46:
        i = 65
    elif i==44:
        i = 57
    elif i == 64:
        i = 45
    elif i == 47:
        i = 90
    elif len(room)==6:
        sense.show_message(room, scroll_speed=0.04, text_colour=[255,125,0])
        AssignRoom = False
        TempRead = True
    else:
        character = chr(i)
        sense.show_letter(character)
    for event in sense.stick.get_events():

        if event.direction == "up" and (event.action == "pressed" or event.action == "held"):
            i = i+1

        elif event.direction == "down" and (event.action == "pressed" or event.action == "held"):
            i = i-1

        elif event.direction == "middle" and event.action == "pressed":
            room = room + character
            sense.show_letter(character, text_colour=[0,255,0])
            sleep(0.5)

Average_list = []
total = 0

while TempRead:
    if len(Average_list) == 10:
        Average_list = []
        total = 0
    temp = sense.get_temperature()
    diff = round(cpu.temperature - temp, 1)
    Average_list += [diff]
    total += diff
    average = total/len(Average_list)
    temp = (temp - average)*(9/5)+32
    temp = round(temp,1)
    #print("Average: " + str(average))
    #print("total: " + str(total))

    #print(temp)
    
    sense.show_message(str(temp)+ "F")
    
    info = json.dumps({"Room": room, "Temp": temp})
    client.publish("PiTemps", info)
    sleep(2)
    
    
