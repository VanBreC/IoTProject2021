import time
from Arm_Lib import Arm_Device
 
# get a robotic arm object
Arm = Arm_Device()
time.sleep(.1)


# Read the angle value of all servos and print out
def main():
 
    while True:
        for i in range(6):
            aa = Arm.Arm_serial_servo_read(i+1)
            print(aa)
            time.sleep(.01)
        time.sleep(.5)
        print(" END OF LINE! ")
 
    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass



# After controlling the movement of a servo individually, read its angle
#id = 6
#angle = 150
 
#Arm.Arm_serial_servo_write(id, angle, 500)
#time.sleep(1)
 
#aa = Arm.Arm_serial_servo_read(id)
#print(aa)
 
time.sleep(.5)

del Arm  # Release the Arm object
