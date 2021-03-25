from time import sleep
sleep(3)
from sense_hat import SenseHat
sense = SenseHat()
import subprocess

Loop = True


#To run on start up, enter command sudo crontab -e
#Choose nano
#Add to end of file @reboot python3 /home/pi/Documents/IoTProject2021/ShowIpOnStart.py
while Loop:
    res = str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")
    if res[0:3] != "192":
        sense.show_message("Connecting...", scroll_speed=0.05)
    else:
        sense.show_message(res)
    #print (res.split(".")[3])
    for event in sense.stick.get_events():
        if event.direction == "middle" and (event.action == "pressed" or event.action == "held"):
            Loop = False
