from sense_hat import SenseHat
sense = SenseHat()
from time import sleep
from random import choice

sense.clear()

GameStart = False
Wait = True
Direction = ""

SnakeHeadx = 1
SnakeHeady = 3
Score = 0
SnakeBodyx = [1]
SnakeBodyy = [3]

Fruitx = 6
Fruity = 3

#sense.set_pixel(column, row, (r, g, b))
sense.set_pixel(SnakeHeadx, SnakeHeady, (0, 255, 0))
sense.set_pixel(Fruitx, Fruity, (255, 0, 0))

while Wait:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            Direction = str(event.direction)
            #print (Direction)
            GameStart = True
            Wait = False

while GameStart:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            Direction = str(event.direction)

    x = 0
    y = 0
    if Direction == "right":
        x = x+1
    elif Direction == "left":
        x = x-1
    elif Direction == "up":
        y = y-1
    elif Direction == "down":
        y = y+1

    if x or y != 0:
        SnakeHeadx = SnakeHeadx+x
        SnakeBodyx.append(SnakeHeadx)
        SnakeHeady = SnakeHeady+y
        SnakeBodyy.append(SnakeHeady)
        sense.set_pixel(SnakeHeadx, SnakeHeady, (0, 255, 0))
        sense.set_pixel(SnakeBodyx[0], SnakeBodyy[0], (0, 0, 0))
        if Score < (len(SnakeBodyx) and len(SnakeBodyy)):
            del SnakeBodyx[0]
            del SnakeBodyy[0]

        if SnakeHeadx == Fruitx and SnakeHeady == Fruity:
            Score = Score+1
            SnakeBodyx.insert(1,SnakeBodyx[0])
            SnakeBodyy.insert(1,SnakeBodyy[0])
            oldFruitx = Fruitx
            oldFruity = Fruity
            while (oldFruitx == Fruitx and oldFruity == Fruity) or (Fruitx in SnakeBodyx and SnakeBodyy[SnakeBodyx.index(Fruitx)] == Fruity) or (Fruity in SnakeBodyy and SnakeBodyx[SnakeBodyy.index(Fruity)] == Fruitx):
                Fruitx = choice([0, 1, 2, 3, 4, 5, 6, 7])
                Fruity = choice([0, 1, 2, 3, 4, 5, 6, 7])
            sense.set_pixel(Fruitx, Fruity, (255, 0, 0))
        sleep(1)
