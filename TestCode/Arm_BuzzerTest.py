import time
from Arm_Lib import Arm_Device
 
# Get the object of DOFBOT
Arm = Arm_Device()
time.sleep(.1)


# Buzzer whistle 100 milliseconds
b_time = 1
Arm.Arm_Buzzer_On(b_time)
time.sleep(1)
# Buzzer whistle 300 milliseconds

b_time = 3
Arm.Arm_Buzzer_On(b_time)
time.sleep(1)



# Buzzer whistle all the time
Arm.Arm_Buzzer_On()
time.sleep(1)
# Close buzzer
Arm.Arm_Buzzer_Off()
time.sleep(1)

del Arm  # Release the DOFBOT object
