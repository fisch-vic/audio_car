import RPi.GPIO as GPIO
import time


def init():
    # function to initialize car
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

def exit():
    # function to exit
    GPIO.cleanup()


for pin in hbridge:
    print(pin)
    GPIO.output(hbridge[pin], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(hbridge[pin], GPIO.LOW)
    time.sleep(1)







