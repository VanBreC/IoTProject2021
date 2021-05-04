import time
from Arm_Lib import Arm_Device
 
# Get a robotic arm object
Arm = Arm_Device()
time.sleep(.1)


# Control DOFBOT swing up and down from side to side
def main():
    # Middle servo
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)
 
    while True:
        # Control No. 3 and No.4 servo up and down
        Arm.Arm_serial_servo_write(3, 0, 1000)
        time.sleep(.001)
        Arm.Arm_serial_servo_write(4, 180, 1000)
        time.sleep(1)
        
        # Control No. 1 servo left and right
        Arm.Arm_serial_servo_write(1, 180, 500)
        time.sleep(.5)
        Arm.Arm_serial_servo_write(1, 0, 1000)
        time.sleep(1)
        
        # Control servo to restore initial position
        Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
        time.sleep(1.5)
 
 
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

del Arm  #Release the Arm object
