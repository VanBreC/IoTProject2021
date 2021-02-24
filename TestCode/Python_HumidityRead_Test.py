from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

humidity = sense.get_humidity()
humidity = round(humidity,1)
print(humidity)
sense.show_message("Room-1 " + str(humidity))