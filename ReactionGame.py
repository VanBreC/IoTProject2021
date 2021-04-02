# IMPORT the required libraries (sense_hat, time, random) 
from sense_hat import SenseHat
from time import sleep
from random import choice
import paho.mqtt.client as mqtt
import json
import subprocess

# CREATE a sense object
sense = SenseHat()
broker_address="192.168.1.32"
sship = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")
endofsship = sship.split(".")[3]
client = mqtt.Client("DWF"+endofsship)

# Set up the colours (white, green, red, empty)

o = (255, 165, 0)
w = (150, 150, 150)
g = (0, 255, 0)
r = (255, 0, 0)
b = (0, 0, 255)
e = (0, 0, 0)

# Create images for three different coloured arrows

arrow = [
e,e,e,w,w,e,e,e,
e,e,w,w,w,w,e,e,
e,w,e,w,w,e,w,e,
w,e,e,w,w,e,e,w,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e
]

arrow_red = [
e,e,e,r,r,e,e,e,
e,e,r,r,r,r,e,e,
e,r,e,r,r,e,r,e,
r,e,e,r,r,e,e,r,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e
]

arrow_green = [
e,e,e,g,g,e,e,e,
e,e,g,g,g,g,e,e,
e,g,e,g,g,e,g,e,
g,e,e,g,g,e,e,g,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e
]
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

# Set a variable pause to 3 (the initial time between turns)  
# Set variables score and angle to 0  
# Create a variable called play set to True (this will be used to stop the game later)  
stall = 3
score = 0
angle = 0

sense.show_message("--Navigate With Joystick L R U D - Middle Click Selects--", scroll_speed=0.04, text_colour=b)
sleep(0.5)
sense.show_message("Choose Difficulty", scroll_speed=0.04, text_colour=o)
sense.show_message("Normal (L)", scroll_speed=0.04, text_colour=g)
sense.show_message("Hard (R)", scroll_speed=0.04, text_colour=r)

select = True
for event in sense.stick.get_events():
    continue
sense.show_letter("N", text_colour=g)
difficulty = "N"
while select:
    for event in sense.stick.get_events():
        if event.direction == "left":
            difficulty = "N"
            sense.show_letter(difficulty, text_colour=g)
        elif event.direction == "right":
            difficulty = "H"
            sense.show_letter(difficulty, text_colour=r)
        elif event.direction == "middle":
            if difficulty == "N":
                sense.show_message("Keep Green Arrow Pointing Up", scroll_speed=0.04, text_colour=g)
            elif difficulty == "H":
                sense.show_message("Green Arrows Point Up", scroll_speed=0.04, text_colour=g)
                sense.show_message("Red Arrows Point Down", scroll_speed=0.04, text_colour=r)
            else:
                break
            GameStart = True
            select = False

# WHILE play == True
while GameStart:

    # CHOOSE a new random angle
    last_angle = angle

    if difficulty == "H":
        arrow_choice = choice(["G", "R"])
        if arrow_choice == "G":
            arrow_colour = arrow_green
        elif arrow_choice == "R":
            arrow_colour = arrow_red
    else:
        arrow_choice = "G"
        arrow_colour = arrow_green

    while angle == last_angle:
        angle = choice([0, 90, 180, 270])

    sense.set_rotation(angle)

    # DISPLAY the white arrow
    sense.set_pixels(arrow_colour)

    # SLEEP for current pause length
    sleep(stall)


    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x = round(x, 0)
    y = round(y, 0)

    #print(angle)
    #print(x)
    #print(y)

    # IF orientation matches the arrow...
    if arrow_choice == "G":
        if x == -1 and angle == 90:
            # ADD a point and turn the arrow green
            sense.set_pixels(check_mark)
            score += 1
        elif x == 1 and angle == 270:
            sense.set_pixels(check_mark)
            score += 1
        elif y == -1 and angle == 180:
            sense.set_pixels(check_mark)
            score += 1
        elif y == 1 and angle == 0:
            sense.set_pixels(check_mark)
            score += 1
        else:
            # SET play to `False` and DISPLAY the red arrow
            failed = 1
            for failed in range(10):
                sense.set_pixels(arrow)
                sleep(0.1)
                sense.clear()
                sleep(0.1)
            GameStart = False

    # IF orientation matches the arrow...
    if arrow_choice == "R":
        if x == -1 and angle == 270:
            # ADD a point and turn the arrow green
            sense.set_rotation(90)
            sense.set_pixels(check_mark)
            score += 1
        elif x == 1 and angle == 90:
            sense.set_rotation(270)
            sense.set_pixels(check_mark)
            score += 1
        elif y == -1 and angle == 0:
            sense.set_rotation(180)
            sense.set_pixels(check_mark)
            score += 1
        elif y == 1 and angle == 180:
            sense.set_rotation(0)
            sense.set_pixels(check_mark)
            score += 1
        else:
            # SET play to `False` and DISPLAY the red arrow
            failed = 1
            for failed in range(10):
                sense.set_pixels(arrow)
                sleep(0.1)
                sense.clear()
                sleep(0.1)
            GameStart = False
    #print (stall)
    # Shorten the pause duration slightly  
    stall = stall * 0.95
    
    # Pause before the next arrow 
    sleep(0.5)
    

# When loop is exited, display a message with the score  
msg = "Your score was %s" % score
sense.set_rotation(0)
sense.show_message(msg, scroll_speed=0.04, text_colour=b)

sense.show_message("Save your score?", scroll_speed=0.04, text_colour=b)
sense.show_message("Yes (U)", scroll_speed=0.04, text_colour=g)
sense.show_message("No (D)", scroll_speed=0.04, text_colour=r)

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
                sense.show_letter(chr(i), text_colour=o)
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
        sense.show_message(name + " " + str(score), scroll_speed=0.04, text_colour=o)
        sense.show_message("Thanks For Playing!!!", scroll_speed=0.04, text_colour=b)
        info = json.dumps({"Game": "Reaction", "Difficulty": difficulty, "ID": name, "Score": score})
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
        sense.show_letter(character, text_colour=o)
    for event in sense.stick.get_events():

        if event.direction == "up" and (event.action == "pressed" or event.action == "held"):
            i = i+1

        elif event.direction == "down" and (event.action == "pressed" or event.action == "held"):
            i = i-1

        elif event.direction == "middle" and event.action == "pressed":
            name = name + character
            sense.set_pixels(check_mark)
            sleep(0.5)
