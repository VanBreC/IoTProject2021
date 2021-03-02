# IMPORT the required libraries (sense_hat, time, random) 
from sense_hat import SenseHat
from time import sleep
from random import choice
import paho.mqtt.client as mqtt
import json

# CREATE a sense object
sense = SenseHat()
broker_address="192.168.1.32"
client = mqtt.Client("DWF")
client.connect(broker_address)

# Set up the colours (white, green, red, empty)

w = (150, 150, 150)
g = (0, 255, 0)
r = (255, 0, 0)
e = (0, 0, 0)

# Create images for three different coloured arrows

normal = "N"
hard = "H"

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
sense.show_message("Select with Joystick", scroll_speed=0.04, text_colour=[0,0,255])
sense.show_message("Normal (Left)", scroll_speed=0.04, text_colour=[0,255,0])
sense.show_message("or", scroll_speed=0.04, text_colour=[0,0,255])
sense.show_message("Hard (Right)", scroll_speed=0.04, text_colour=[255,0,0])

select = True
for event in sense.stick.get_events():
    continue
sense.show_letter(normal, text_colour=[0,255,0])
difficulty = "N"
while select:
    for event in sense.stick.get_events():
        if event.direction == "left":
            difficulty = "N"
            sense.show_letter(normal, text_colour=[0,255,0])
        elif event.direction == "right":
            difficulty = "H"
            sense.show_letter(hard, text_colour=[255,0,0])
        elif event.direction == "middle":
            if difficulty == normal:
                sense.show_message("Keep green arrow up", scroll_speed=0.04, text_colour=[0,255,0])
                normal_difficulty = True
                hard_difficulty = False
                select = False
            elif difficulty == hard:
                sense.show_message("Green Arrows Up", scroll_speed=0.04, text_colour=[0,255,0])
                sense.show_message("Red Arrows Down", scroll_speed=0.04, text_colour=[255,0,0])
                hard_difficulty = True
                normal_difficulty = False
                select = False
            else:
                break

# WHILE play == True 
while normal_difficulty:
  
    # CHOOSE a new random angle 
    last_angle = angle
    while angle == last_angle:
        angle = choice([0, 90, 180, 270])
        
    sense.set_rotation(angle)
    
    # DISPLAY the white arrow
    sense.set_pixels(arrow_green)
    
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
        normal_difficulty = False

    # Shorten the pause duration slightly  
    stall = stall * 0.95
    
    # Pause before the next arrow 
    sleep(0.5)
    
    
while hard_difficulty:
  
    # CHOOSE a new random angle 
    last_angle = angle
    while angle == last_angle:
        arrow_choice = choice(["G", "R"])
        if arrow_choice == "G":
            arrow_colour = arrow_green
        elif arrow_choice == "R":
            arrow_colour = arrow_red
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
            normal_difficulty = False
    
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
            hard_difficulty = False

    # Shorten the pause duration slightly  
    stall = stall * 0.95
    
    # Pause before the next arrow 
    sleep(0.5)
    

# When loop is exited, display a message with the score  
msg = "Your score was %s" % score
sense.set_rotation(0)
sense.show_message(msg, scroll_speed=0.04, text_colour=[0, 0, 255])

sense.show_message("Would you like to save your score? Joystick: Yes/Up No/Down", scroll_speed=0.04, text_colour=[100,100,100])

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
                sense.show_message("Select Three Characters as Your Name", scroll_speed=0.04, text_colour=[0,0,255])
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
        i == 65
    elif i == 64:
        i = 57
    elif i == 47:
        i = 90
    elif len(name)==3:
        sense.show_message(name + " " + str(score), scroll_speed=0.04, text_colour=[255,255,0])
        sense.show_message("Thanks For Playing!!!", scroll_speed=0.04, text_colour=[0,0,255])
        info = json.dumps({"ID": name, "Score": score})
        client.publish("testarrowgame", info)
        LeaderBoard = False
    else:
        character = chr(i)
        sense.show_letter(character)
    for event in sense.stick.get_events():

        if event.direction == "up" and event.action == "pressed":
            i = i+1

        elif event.direction == "down" and event.action == "pressed":
            i = i-1

        elif event.direction == "middle" and event.action == "pressed":
            name = name + character
            sense.set_pixels(check_mark)
            sleep(0.5)
