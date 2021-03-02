from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

sense.clear()

w = (150, 150, 150)
g = (0, 255, 0)
r = (255, 0, 0)
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

i = 65
Name = ""
sense.show_letter(chr(i))
#for i in range(123):
    #print(str(i) + ": " + chr(i))
while True:
    if i==91:
        i = 48
    elif i==58:
        i == 65
    elif i == 64:
        i = 57
    elif i == 47:
        i = 90
    elif len(Name)==3:
        sense.show_message(Name + " " + "38")
    else:
        character = chr(i)
        sense.show_letter(character)
    for event in sense.stick.get_events():
        #print(event, event.direction, event.action)
        
        if event.direction == "up" and event.action == "pressed":
            i = i+1
            #sense.show_letter(chr(i))
        elif event.direction == "down" and event.action == "pressed":
            i = i-1
            #sense.show_letter(chr(i))
        #elif event.direction == "left":
            #sense.show_letter("L")
        #elif event.direction == "right":
            #sense.show_letter("R")
        elif event.direction == "middle" and event.action == "pressed":
            Name = Name + character
            sense.set_pixels(check_mark)
        
        sleep(0.5)
        sense.clear()
