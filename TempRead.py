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

#priority = ""
room = ""
Average_list = []
List_Pos = 0
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
    global List_Pos
    global total
    temp = sense.get_temperature()
    diff = float(round(cpu.temperature - temp, 1))
    if List_Pos > 9:
        List_Pos = 0
    if len(Average_list) == 10:
        Average_list[List_Pos] = diff
        List_Pos += 1
        total = sum(Average_list)
        #TempRead = False
    else:
        Average_list.append(diff)
        total += diff

    average = total/len(Average_list)
    temp = (temp - average)*(9/5)+32
    temp = round(temp,1)
    #print("Average: " + str(average))
    #print("total: " + str(total))
    #print(Average_list)
    #print(temp)

    sense.show_message(str(temp)+ "F")
    info = json.dumps({"PiNumber": pinumber, "Room": room, "Temp": temp})
    client.publish("PiTemps", info)
    sleep(1)

"""def on_connect(client, userdata, flags, rc):
    print ("Connected with result code "+str(rc))
    client.subscribe("ReturnPiTemps")
    client.publish("Start", "Pi " + Identify() + " Started Reading Temps")"""

"""def on_message(client, userdata, msg):
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
    TempRead(client=client)"""

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

pinumber = Identify()

SetRoom()

#client.on_connect = on_connect
#client.on_message = on_message

#client.loop_forever()

#ClientConnect(broker_address)

Loop = True

while Loop:
    end = 0
    TempRead(client)
    for event in sense.stick.get_events():
        if event.direction == "middle":
            end += 1
    if end >= 10:
        print("Ending Program")
        Loop = False
        break
