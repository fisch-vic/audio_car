import RPi.GPIO as GPIO
import time


Pin1 = 18
Pin2 = 22

def forward():
    GPIO.output(Pin1, GPIO.HIGH)
    GPIO.output(Pin2, GPIO.LOW)

def backward():
    GPIO.output(Pin1, GPIO.LOW)
    GPIO.output(Pin2, GPIO.HIGH)

def stop():
    GPIO.output(Pin1, GPIO.LOW)
    GPIO.output(Pin2, GPIO.LOW)

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Pin1, GPIO.OUT)
    GPIO.setup(Pin2, GPIO.OUT)

print ("starting")
setup()
while True:
    print ("forward")
    forward()
    time.sleep(2)
    print ("backward")
    backward()
    time.sleep(2)
    print("stop")
    stop()
    time.sleep(2)
