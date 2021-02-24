from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

pressure = sense.get_pressure()
pressure = round(pressure,1)
print(pressure)
sense.show_message("Room-1 " + str(pressure))