from sense_hat import SenseHat
import time

sense = SenseHat()
#LED's are graphed as X (left to right) 0-8 and Y (top to bottom) 0-8

sense.clear()
sense.set_pixel(2, 2, [0,0,255])
sense.set_pixel(4, 2, [0,0,255])
sense.set_pixel(3, 4, [100,0,0])
sense.set_pixel(1, 5, [255,0,0])
sense.set_pixel(2, 6, [255,0,0])
sense.set_pixel(3, 6, [255,0,0])
sense.set_pixel(4, 6, [255,0,0])
sense.set_pixel(5, 5, [255,0,0])
pixel_list = sense.get_pixels()
print(pixel_list)

time.sleep(10)

r = [255,0,0]
o = [255,127,0]
y = [255,255,0]
g = [0,255,0]
b = [0,0,255]
i = [75,0,130]
v = [159,0,255]
e = [0,0,0]

image=[e,e,e,e,e,e,e,e,e,e,e,r,r,e,e,e,e,r,r,o,o,r,r,e,r,o,o,y,y,o,o,r,o,y,y,g,g,y,y,o,y,g,g,b,b,g,g,y,b,b,b,i,i,b,b,b,b,i,i,v,v,i,i,b]
sense.set_pixels(image)
time.sleep(3)
#sense.flip_h() Flips image Horizontally
#sense.flip_v() Flips image Vertically
sense.set_rotation(90)
time.sleep(1)
sense.set_rotation(180)
time.sleep(1)
sense.set_rotation(270)
time.sleep(1)
sense.set_rotation(0)
time.sleep(5)
sense.clear()
