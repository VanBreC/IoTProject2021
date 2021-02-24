from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

sense.clear()
while True:
    for event in sense.stick.get_events():
        print(event.direction, event.action)
        
        if event.direction == "up":
            sense.show_letter("U")
        elif event.direction == "down":
            sense.show_letter("D")
        elif event.direction == "left":
            sense.show_letter("L")
        elif event.direction == "right":
            sense.show_letter("R")
        elif event.direction == "middle":
            sense.show_letter("M")
        
        sleep(0.5)
        sense.clear()