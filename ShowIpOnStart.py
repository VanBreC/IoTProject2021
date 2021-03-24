from time import sleep
sleep(3)
from sense_hat import SenseHat
sense = SenseHat()
import subprocess

Loop = True

while Loop:
    res = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")
    sense.show_message(res)
    for event in sense.stick.get_events():
        if event.direction == "middle" and (event.action == "pressed" or event.action == "held"):
            Loop = False
