import time
from Arm_Lib import Arm_Device
 
# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)
 
def main():
    while True:
        Arm.Arm_RGB_set(50, 0, 0) #red
        time.sleep(.5)
        Arm.Arm_RGB_set(0, 50, 0) #green
        time.sleep(.5)
        Arm.Arm_RGB_set(0, 0, 50) #blue
        time.sleep(.5)
 
        print(" END OF LINE! ")
 
try :
    main()
except KeyboardInterrupt:
    # Release DOFBOT object
    del Arm
    print(" Program closed! ")
    pass
