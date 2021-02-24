from sense_hat import SenseHat

sense = SenseHat()


sense.show_letter("1",text_colour=[255,0,0])
#sense.clear()

#sense orientation
while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    
    x=round(x,0)
    y=round(y,0)
    z=round(z,0)
    
    print("x={0}, y={1}, z={2}".format(x,y,z))
    
    
    #rotate image/text based on device orientation
    if x == -1:
        sense.set_rotation(90)
    elif y == 1:
        sense.set_rotation(0)
    elif y == -1:
        sense.set_rotation(180)
    elif x== 1:
        sense.set_rotation(270)
    else:
        sense.set_rotation(0)