from sense_hat import SenseHat
sense = SenseHat()
import paho.mqtt.client as mqtt
from time import sleep
import json
import subprocess
import os
from gpiozero import CPUTemperature
cpu = CPUTemperature()
sense.clear()

priority = ""
room = ""
Average_list = []
total = 0
broker_address="192.168.1.32"

def Identify():
    sship = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")
    endofsship = sship.split(".")[3]
    return endofsship

def SetRoom():
        global room
        i=65
        AssignRoom = True
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


def TempRead(client):
    global Average_list
    global total
    if len(Average_list) == 10:
        Average_list = []
        total = 0
        TempRead = False
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
    info = json.dumps({"Priority": priority, "Room": room, "Temp": temp})
    client.publish("PiTemps", info)
    sleep(2)

def on_connect(client, userdata, flags, rc):
    print ("Connected with result code "+str(rc))
    client.subscribe("ReturnPiTemps")
    client.publish("Start", "Pi " + Identify() + " Started Reading Temps")

def on_message(client, userdata, msg):
    global priority
    if str(msg.payload.decode("UTF-8")) == ("Pi " + Identify() + " Started Reading Temps"):
        pass
    else:
        if priority != str(msg.payload.decode("UTF-8")).split('"')[3]:
            print("yes")
            priority = str(msg.payload.decode("UTF-8")).split('"')[3]
            print (priority)
        else:
            print (str(msg.payload.decode("UTF-8")).split('"')[3])
            print ("Topic: {} / Message: {}".format(msg.topic,str(msg.payload.decode("UTF-8"))))
            print ("Non Message")
            client.disconnect()
            #client.loop_stop()
    TempRead(client=client)

client = mqtt.Client("DWF"+Identify())

def ClientConnect(broker_address):
    try:
        client.connect(broker_address)
    except OSError:
        print("Failed to connect to Server | Attempting connection to local VM")
        broker_address="192.168.1.18"
        client.connect(broker_address)
    except:
        print("Both Connections Failed")

ClientConnect(broker_address)

SetRoom()

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

ClientConnect(broker_address)

Loop = True

while Loop:
    
    TempRead(client)
