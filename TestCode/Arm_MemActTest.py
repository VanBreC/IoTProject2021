import time
from Arm_Lib import Arm_Device
 
# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)


# Open the study mode, the RGB light on the expansion board will keep breathing light, and all the servos of the DFOBOT will close the torque.
# At this point, we can manually control the DFOBOT to complete some actions
Arm.Arm_Button_Mode(1)


# In the study mode, every time you run this cell, the current action is recorded and saved, and the RGB lights on the expansion board will switch colors.
# If the red breathing light appears, it means that the learned action group is full (20 groups).
# This command can also be replaced by pressing the K1 button on the expansion board.
Arm.Arm_Action_Study()


# Close study mode and breathing light will be closed
Arm.Arm_Button_Mode(0)


# Read the number of currently recorded action groups
num = Arm.Arm_Read_Action_Num()
print(num)


# Run action group single
Arm.Arm_Action_Mode(1)


# Run action group in loop
Arm.Arm_Action_Mode(2)


# Stop action group
Arm.Arm_Action_Mode(0)


# Clear the action group, the RGB light on the expansion board will be green when the clearing is completed.
# Note: Once the recorded action group is cleared, it cannot be restored.
Arm.Arm_Clear_Action()

del Arm   # Release DOFBOT object
