import time
from Arm_Lib import Arm_Device
 
# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)


# Separately control a servo to move to a certain angle
id = 5
#print("Move Servo 5 to 90") 
#Arm.Arm_serial_servo_write(4, 90, 500)
time.sleep(1)


# Separately control a servo to move to a certain angle
id = 5
#print("Move Servo 5 to 180")
#Arm.Arm_serial_servo_write(id, 180, 5)
time.sleep(1)



# Control a servo to switch angles
id = 5
 
def main():
    for i in range(5):
        Arm.Arm_serial_servo_write(2, 60, 500)
        Arm.Arm_serial_servo_write6(45, 45, 45, 45, 45, 45, 0)
        ServoAngle = Arm.Arm_serial_servo_read(i+1)
        print("Adjusting Servo ", i+1)
        while ServoAngle not in range(44,47):
            Arm.Arm_serial_servo_write(i+1, 45, 0)
            ServoAngle = Arm.Arm_serial_servo_read(i+1)
        print("Servo ", i+1, " is now adjusted")
        time.sleep(3)
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass


del Arm  # Release the Arm object
