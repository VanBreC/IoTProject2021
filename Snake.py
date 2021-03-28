from sense_hat import SenseHat
sense = SenseHat()
from time import sleep
from random import choice
import paho.mqtt.client as mqtt
import json
import subprocess

sense.clear()

broker_address="192.168.1.32"
sship = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")
endofsship = sship.split(".")[3]
client = mqtt.Client("DWF"+endofsship)

g = (0, 255, 0)
e = (0, 0, 0)

check_mark = [
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,g,
e,e,e,e,e,e,g,e,
e,e,e,e,e,g,e,e,
g,e,e,e,g,e,e,e,
e,g,e,g,e,e,e,e,
e,e,g,e,e,e,e,e
]

GameStart = False
Wait = True
Direction = ""

SnakeHeadx = 1
SnakeHeady = 3
Score = 0
SnakeBodyx = [1]
SnakeBodyy = [3]
SnakeBodyPos = [13]

Fruitx = 6
Fruity = 3

#sense.set_pixel(column, row, (r, g, b))
sense.set_pixel(SnakeHeadx, SnakeHeady, (0, 255, 0))
sense.set_pixel(Fruitx, Fruity, (255, 0, 0))

while Wait:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            Direction = str(event.direction)
            PrevDirection = ""
            #print (Direction)
            GameStart = True
            Wait = False

while GameStart:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            PrevDirection = Direction
            Direction = str(event.direction)

    x = 0
    y = 0
    if (Direction == "right") and (PrevDirection != "left"):
        x = x+1
    elif (Direction == "left") and (PrevDirection != "right"):
        x = x-1
    elif (Direction == "up") and (PrevDirection != "down"):
        y = y-1
    elif (Direction == "down") and (PrevDirection != "up"):
        y = y+1
    else:
        Direction = PrevDirection

    if x or y != 0:
        SnakeHeadx = SnakeHeadx+x
        SnakeBodyx.append(SnakeHeadx)
        SnakeHeady = SnakeHeady+y
        SnakeBodyy.append(SnakeHeady)
        SnakeBodyPos.append(int(str(SnakeHeadx)+str(SnakeHeady)))
        if (SnakeBodyPos.count(int(str(SnakeHeadx)+str(SnakeHeady))) > 1) or (SnakeHeadx < 0 or SnakeHeadx > 7) or (SnakeHeady < 0 or SnakeHeady > 7):
            sense.show_message("Game Over", scroll_speed=0.05)
            sense.show_message("Your Score was " + str(Score), scroll_speed=0.05)
            GameStart = False
            break
        sense.set_pixel(SnakeHeadx, SnakeHeady, (0, 255, 0))
        sense.set_pixel(SnakeBodyx[0], SnakeBodyy[0], (0, 0, 0))
        if Score < (len(SnakeBodyx) and len(SnakeBodyy)):
            del SnakeBodyx[0]
            del SnakeBodyy[0]
            del SnakeBodyPos[0]

        if SnakeHeadx == Fruitx and SnakeHeady == Fruity:
            Score = Score+1
            SnakeBodyx.insert(1,SnakeBodyx[0])
            SnakeBodyy.insert(1,SnakeBodyy[0])
            SnakeBodyPos.insert(1,SnakeBodyPos[0])
            FruitPos = int(str(Fruitx)+str(Fruity))
            while FruitPos in SnakeBodyPos:
                Fruitx = choice([0, 1, 2, 3, 4, 5, 6, 7])
                Fruity = choice([0, 1, 2, 3, 4, 5, 6, 7])
                FruitPos = int(str(Fruitx)+str(Fruity))
            sense.set_pixel(Fruitx, Fruity, (255, 0, 0))
        sleep(0.5)

sense.show_message("Save your score?", scroll_speed=0.04, text_colour=[0,0,255])
sense.show_message("Yes (U)", scroll_speed=0.04, text_colour=[0,255,0])
sense.show_message("No (D)", scroll_speed=0.04, text_colour=[255,0,0])

for event in sense.stick.get_events():
    continue

sense.show_letter("Y", text_colour=[0,255,0])
Keep = "Y"

LeaderBoard = False
Save = True

while Save:
    for event in sense.stick.get_events():
        if event.direction == "up":
            sense.show_letter("Y", text_colour=[0,255,0])
            Keep = "Y"
        elif event.direction == "down":
            sense.show_letter("N", text_colour=[255,0,0])
            Keep = "N"
        elif event.direction == "middle":
            if Keep == "Y":
                sense.show_message("Select Three Characters", scroll_speed=0.04, text_colour=[0,0,255])
                LeaderBoard = True
                name = ""
                i = 65
                sense.show_letter(chr(i))
                Save = False
            elif Keep == "N":
                sense.show_message("Thanks For Playing!!!", scroll_speed=0.04, text_colour=[0,0,255])
                Save = False
            else:
                continue


while LeaderBoard:
    if i==91:
        i = 48
    elif i==58:
        i = 65
    elif i == 64:
        i = 57
    elif i == 47:
        i = 90
    elif len(name)==3:
        sense.show_message(name + " " + str(Score), scroll_speed=0.04, text_colour=[255,125,0])
        sense.show_message("Thanks For Playing!!!", scroll_speed=0.04, text_colour=[0,0,255])
        info = json.dumps({"Game": "Snake", "ID": name, "Score": Score})
        #print (info)
        sleep(0.25)
        try:
            client.connect(broker_address)
        except OSError:
            print("Failed to connect to Server | Attempting connection to local VM")
            broker_address="192.168.1.10"
            client.connect(broker_address)
        except:
            print("Both Connections Failed")
            LeaderBoard = False
            break
        sleep(0.25)
        client.publish("GameScores", info)
        LeaderBoard = False
    else:
        character = chr(i)
        sense.show_letter(character)
    for event in sense.stick.get_events():

        if event.direction == "up" and (event.action == "pressed" or event.action == "held"):
            i = i+1

        elif event.direction == "down" and (event.action == "pressed" or event.action == "held"):
            i = i-1

        elif event.direction == "middle" and event.action == "pressed":
            name = name + character
            sense.set_pixels(check_mark)
            sleep(0.5)
