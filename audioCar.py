import RPi.GPIO as GPIO
import time


# GPIO uses pin number
GPIO.setmode(GPIO.BOARD)

# hbridge pin definitions:

hbridge = {"1A":7,"2A":11,"3A":13,"4A":15}

# hbridge GPIO init
for pin in hbridge:
    # set as ouptut
    GPIO.setup(hbridge[pin], GPIO.OUT)
    # set low
    GPIO.output(hbridge[pin], GPIO.LOW)

for pin in hbridge:
    print(pin)
    GPIO.output(hbridge[pin], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(hbridge[pin], GPIO.LOW)
    time.sleep(1)


GPIO.cleanup()







