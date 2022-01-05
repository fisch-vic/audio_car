import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
import wiggle




ledpin = 33
ledpin2 = 19
ledpin3 = 21
bit1 = 35
bit2 = 37
peak = 31
rstSwitch=40

GPIO.setup(ledpin, GPIO.OUT)
GPIO.setup(ledpin2, GPIO.OUT)
GPIO.setup(bit1, GPIO.IN)
GPIO.setup(bit2, GPIO.IN)
GPIO.setup(peak, GPIO.OUT)
GPIO.setup(rstSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(33, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)

def check():
    if(GPIO.input(bit1) and GPIO.input(bit2)):
        wiggle.forward()
        sleep(1)
    #else if(not GPIO.input(bit1) and GPIO.input(bit2)):
       # wiggle.forward()
        #sleep(.5)

def reset():
    GPIO.output(peak,1)
    sleep(.1)

while True:
    
    reset()
    
    #GPIO.output(peak, GPIO.input(rstSwitch))
    GPIO.output(peak,0)
    sleep(.5) 
    if(GPIO.input(bit1)):
        GPIO.output(ledpin,1)
    else:
        GPIO.output(ledpin,0)

    if(GPIO.input(bit2)):
        GPIO.output(ledpin3, 1)
    else:
        GPIO.output(ledpin3,0)

    if(not GPIO.input(bit1) and not GPIO.input(bit2)):
        GPIO.output(ledpin2, 1)
    else:
        GPIO.output(ledpin2,0)

    sleep(2)
