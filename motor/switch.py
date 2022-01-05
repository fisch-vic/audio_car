import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
import wiggle


ledpin = 33
ledpin2 =19
ledpin3 =21

switchPin1=36
switchPin2=38
switchPin3=40


GPIO.setup(ledpin, GPIO.OUT)
GPIO.setup(switchPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switchPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switchPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(33,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(19,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(21,GPIO.OUT, initial=GPIO.LOW)


while True:
    #GPIO.output(ledpin, GPIO.input(switchPin1))  
    #GPIO.output(ledpin2, GPIO.input(switchPin2))  
    #GPIO.output(ledpin3, GPIO.input(switchPin3))  
    if(GPIO.input(ledpin)):
        sleep(1)
        #wiggle.square()
    else:
        wiggle.stop()

    if(GPIO.input(ledpin2)):
        sleep(1)
       # wiggle.fig8()
    else:
        wiggle.stop()

    if(GPIO.input(ledpin3)):
        sleep(1)
        #wiggle.forward()
    else:
        wiggle.stop()


    sleep(0.2)
