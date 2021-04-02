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

o = (255,165,0)
g = (0, 255, 0)
r = (255,0,0)
b = (0,0,255)
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

#sense.set_pixel(column, row, (r, g, b))

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

TotalMovement = 0

while Wait:
    sense.show_message("--Middle Click Joystick For Rules | Push Any Direction To Start--", scroll_speed=0.04, text_colour=b)
    sleep(1)
    sleep(1)
    sleep(1)
    for event in sense.stick.get_events():
        if event.direction == "middle":
            sense.show_message("Collect The Fruit | Dont Collide Into Your Body or The Edge", scroll_speed=0.04, text_colour=o)
            sleep(1.5)
            sense.show_message("Game Start", scroll_speed=0.04, text_colour=b)
            Direction = "right"
            sense.set_pixel(SnakeHeadx, SnakeHeady, g)
            sense.set_pixel(Fruitx, Fruity, r)
            sleep(2)
            GameStart = True
            Wait = False
            break
        elif (event.direction != "middle") and (event.action == "pressed"):
            Direction = str(event.direction)
            #print (Direction)
            sense.set_pixel(SnakeHeadx, SnakeHeady, g)
            sense.set_pixel(Fruitx, Fruity, r)
            sleep(2)
            GameStart = True
            Wait = False
            break

while GameStart:
    DirectionList = []
    for event in sense.stick.get_events():
        if event.action == "pressed":
            DirectionList.append(event.direction)
            if (DirectionList[0] == "right") and (Direction != "left"):
                Direction = DirectionList[0]
            elif (DirectionList[0] == "left") and (Direction != "right"):
                Direction = DirectionList[0]
            elif (DirectionList[0] == "up") and (Direction != "down"):
                Direction = DirectionList[0]
            elif (DirectionList[0] == "down") and (Direction != "up"):
                Direction = DirectionList[0]
            else:
                continue

    x = 0
    y = 0
    if (Direction == "right"):
        x = x+1
    elif (Direction == "left"):
        x = x-1
    elif (Direction == "up"):
        y = y-1
    elif (Direction == "down"):
        y = y+1
    else:
        continue



    if x or y == 1 or -1:
        SnakeHeadx = SnakeHeadx+x
        SnakeBodyx.append(SnakeHeadx)
        SnakeHeady = SnakeHeady+y
        SnakeBodyy.append(SnakeHeady)
        #print ("X: ", SnakeHeadx, "\nY: ", SnakeHeady)
        SnakeBodyPos.append(str(SnakeHeadx)+str(SnakeHeady))
        if (SnakeBodyPos.count(str(SnakeHeadx)+str(SnakeHeady)) > 1) or (SnakeHeadx < 0 or SnakeHeadx > 7) or (SnakeHeady < 0 or SnakeHeady > 7):
            if SnakeHeadx == -1:
                SnakeHeadx = SnakeHeadx + 1
            elif SnakeHeadx == 8:
                SnakeHeadx = SnakeHeadx - 1
            elif SnakeHeady == -1:
                SnakeHeady = SnakeHeady + 1
            elif SnakeHeady == 8:
                SnakeHeady = SnakeHeady - 1
            for i in range(10):
                sense.set_pixel(SnakeHeadx, SnakeHeady, e)
                sleep(0.1)
                sense.set_pixel(SnakeHeadx, SnakeHeady, g)
                sleep(0.1)
            sense.show_message("Game Over", scroll_speed=0.05, text_colour=r)
            sense.show_message("Your Score was " + str(Score), scroll_speed=0.05, text_colour=b)
            GameStart = False
            break
        sense.set_pixel(SnakeHeadx, SnakeHeady, g)
        sense.set_pixel(SnakeBodyx[0], SnakeBodyy[0], e)
        del SnakeBodyx[0]
        del SnakeBodyy[0]
        del SnakeBodyPos[0]

        if SnakeHeadx == Fruitx and SnakeHeady == Fruity:
            Score = Score+1
            #print (Score)
            if Score == 63:
                for i in range(10):
                    sense.clear()
                    sleep(0.1)
                    sense.clear(g)
                    sleep(0.1)
                sense.show_message("Perfect Snake 63 Points!!!", scroll_speed=0.05, text_colour=b)
                GameStart = False
                break
            SnakeBodyx.insert(1,SnakeBodyx[0])
            SnakeBodyy.insert(1,SnakeBodyy[0])
            SnakeBodyPos.insert(1,SnakeBodyPos[0])
            FruitPos = str(Fruitx)+str(Fruity)
            while FruitPos in SnakeBodyPos:
                Fruitx = choice([0, 1, 2, 3, 4, 5, 6, 7])
                Fruity = choice([0, 1, 2, 3, 4, 5, 6, 7])
                FruitPos = str(Fruitx)+str(Fruity)
            sense.set_pixel(Fruitx, Fruity, r)
        TotalMovement = TotalMovement + 1
        sleep(0.5)

sense.show_message("Save your score?", scroll_speed=0.04, text_colour=b)
sense.show_message("Yes (U)", scroll_speed=0.04, text_colour=g)
sense.show_message("No (D)", scroll_speed=0.04, text_colour=r)
sense.show_message("Middle Selects", scroll_speed=0.04, text_colour=b)

for event in sense.stick.get_events():
    continue

sense.show_letter("Y", text_colour=g)
Keep = "Y"

LeaderBoard = False
Save = True

while Save:
    for event in sense.stick.get_events():
        if event.direction == "up":
            sense.show_letter("Y", text_colour=g)
            Keep = "Y"
        elif event.direction == "down":
            sense.show_letter("N", text_colour=r)
            Keep = "N"
        elif event.direction == "middle":
            if Keep == "Y":
                sense.show_message("Select Three Characters", scroll_speed=0.04, text_colour=b)
                LeaderBoard = True
                name = ""
                i = 65
                sense.show_letter(chr(i))
                Save = False
            elif Keep == "N":
                sense.show_message("Thanks For Playing!!!", scroll_speed=0.04, text_colour=b)
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
        sense.show_message(name + " " + str(Score), scroll_speed=0.04, text_colour=o)
        sense.show_message("Thanks For Playing!!!", scroll_speed=0.04, text_colour=b)
        info = json.dumps({"Game": "Snake", "ID": name, "Score": Score, "Movement": TotalMovement})
        #print (info)
        sleep(0.25)
        try:
            client.connect(broker_address)
        except OSError:
            print("Failed to connect to Server | Attempting connection to local VM")
            broker_address="192.168.1.18"
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
        sense.show_letter(character, o)
    for event in sense.stick.get_events():

        if event.direction == "up" and (event.action == "pressed" or event.action == "held"):
            i = i+1

        elif event.direction == "down" and (event.action == "pressed" or event.action == "held"):
            i = i-1

        elif event.direction == "middle" and event.action == "pressed":
            name = name + character
            sense.set_pixels(check_mark)
            sleep(0.5)
