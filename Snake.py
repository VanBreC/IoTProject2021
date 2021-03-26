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
SnakeBodyPos = [13]

Fruitx = 6
Fruity = 3

#sense.set_pixel(column, row, (r, g, b))
sense.set_pixel(SnakeHeadx, SnakeHeady, (0, 255, 0))
sense.set_pixel(Fruitx, Fruity, (255, 0, 0))

while Wait:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            Direction = str(event.direction)
            PrevDirection = ""
            #print (Direction)
            GameStart = True
            Wait = False

while GameStart:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            PrevDirection = Direction
            Direction = str(event.direction)

    x = 0
    y = 0
    if (Direction == "right") and (PrevDirection != "left"):
        x = x+1
    elif (Direction == "left") and (PrevDirection != "right"):
        x = x-1
    elif (Direction == "up") and (PrevDirection != "down"):
        y = y-1
    elif (Direction == "down") and (PrevDirection != "up"):
        y = y+1
    else:
        Direction = PrevDirection

    if x or y != 0:
        SnakeHeadx = SnakeHeadx+x
        SnakeBodyx.append(SnakeHeadx)
        SnakeHeady = SnakeHeady+y
        SnakeBodyy.append(SnakeHeady)
        SnakeBodyPos.append(int(str(SnakeHeadx)+str(SnakeHeady)))
        if (SnakeBodyPos.count(int(str(SnakeHeadx)+str(SnakeHeady))) > 1) or (SnakeHeadx < 0 or SnakeHeadx > 7) or (SnakeHeady < 0 or SnakeHeady > 7):
            sense.show_message("Game Over", scroll_speed=0.075)
            sense.show_message("Your Score was " + str(Score), scroll_speed=0.075)
            GameStart = False
            break
        sense.set_pixel(SnakeHeadx, SnakeHeady, (0, 255, 0))
        sense.set_pixel(SnakeBodyx[0], SnakeBodyy[0], (0, 0, 0))
        if Score < (len(SnakeBodyx) and len(SnakeBodyy)):
            del SnakeBodyx[0]
            del SnakeBodyy[0]
            del SnakeBodyPos[0]

        if SnakeHeadx == Fruitx and SnakeHeady == Fruity:
            Score = Score+1
            SnakeBodyx.insert(1,SnakeBodyx[0])
            SnakeBodyy.insert(1,SnakeBodyy[0])
            SnakeBodyPos.insert(1,SnakeBodyPos[0])
            FruitPos = int(str(Fruitx)+str(Fruity))
            while FruitPos in SnakeBodyPos:
                Fruitx = choice([0, 1, 2, 3, 4, 5, 6, 7])
                Fruity = choice([0, 1, 2, 3, 4, 5, 6, 7])
                FruitPos = int(str(Fruitx)+str(Fruity))
            sense.set_pixel(Fruitx, Fruity, (255, 0, 0))
        sleep(1)
