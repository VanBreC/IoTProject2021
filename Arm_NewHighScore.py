import time
from Arm_Lib import Arm_Device
import paho.mqtt.client as mqtt

# Get a robotic arm object
ArmDance = Arm_Device()
time.sleep(.1)

time_1 = 500
time_2 = 1000
time_sleep = 0.5

broker_address = "192.168.1.32"

# DOFBOT dancing
def main():

    ReturnPosition = []

    for x in range(6):
        Position = ArmDance.Arm_serial_servo_read(x+1)
        if Position == None:
            Position = 90
        ReturnPosition.append(Position)

    #ReturnPosition.reverse()
    #print(ReturnPosition)
    # Middle servo
    ArmDance.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)

    ArmDance.Arm_serial_servo_write(2, 180-120, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 120, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 60, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 180-135, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 135, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 45, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 180-120, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 120, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 60, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 180-80, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 80, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 80, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 180-60, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 60, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 60, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 180-45, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 45, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 45, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(2, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(3, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(.001)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(4, 20, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(6, 150, time_1)
    time.sleep(.001)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(6, 90, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(4, 20, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(6, 150, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(6, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(1, 0, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(5, 0, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(3, 180, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 0, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(6, 180, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(6, 0, time_2)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(6, 90, time_2)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(1, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(5, 90, time_1)
    time.sleep(time_sleep)

    ArmDance.Arm_serial_servo_write(3, 90, time_1)
    time.sleep(.001)
    ArmDance.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(3)

    ArmDance.Arm_serial_servo_write6(ReturnPosition[0], ReturnPosition[1], ReturnPosition[2], ReturnPosition[3], ReturnPosition[4], ReturnPosition[5], 500)


    #print(" END OF LINE! ")

def ClientConnect(broker_address):
    try:
        client.connect(broker_address)
        client.loop_forever()
    except OSError:
        print("Failed to connect to Server | Attempting connection to local VM")
        broker_address="192.168.1.18"
        client.connect(broker_address)
        client.loop_forever()
   # except:
       # print("Both Conections Failed")

def on_connect(client, userdata, flags, rc):
    print ("Connected")
    client.subscribe("NewHighScore")

def on_message(client, userdata, msg):
    print(str(msg.payload.decode("UTF-8")))
    main()



client = mqtt.Client("DOFBOT")

client.on_message = on_message
client.on_connect = on_connect

ClientConnect(broker_address)
