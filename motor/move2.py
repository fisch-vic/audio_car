import RPi.GPIO as GPIO
import time

Pin1 = 12
Pin2 = 16
Pin3 = 18
Pin4 = 11
Pin5 = 13
Pin6 = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Pin1, GPIO.OUT)
GPIO.setup(Pin2, GPIO.OUT)
GPIO.setup(Pin3, GPIO.OUT)
GPIO.setup(Pin4, GPIO.OUT)
GPIO.setup(Pin5, GPIO.OUT)
GPIO.setup(Pin6, GPIO.OUT)

def forward():
    GPIO.output(Pin1, GPIO.HIGH)
    GPIO.output(Pin2, GPIO.LOW)
    GPIO.output(Pin3, GPIO.HIGH)
    
    GPIO.output(Pin4, GPIO.HIGH)
    GPIO.output(Pin5, GPIO.LOW)
    GPIO.output(Pin6, GPIO.HIGH)
def backward():
    GPIO.output(Pin1, GPIO.LOW)
    GPIO.output(Pin2, GPIO.HIGH)
    GPIO.output(Pin3, GPIO.HIGH)

    GPIO.output(Pin4, GPIO.LOW)
    GPIO.output(Pin5, GPIO.HIGH)
    GPIO.output(Pin6, GPIO.HIGH)
def stop():
    GPIO.output(Pin3, GPIO.LOW)
    GPIO.output(Pin6, GPIO.LOW)
def destroy():
    GPIO.cleanup()


print("starting")

while True:
    print("forward")
    forward()
    time.sleep(2)
    print("backward")
    backward()
    time.sleep(2)
    print("stop")
    stop()
    break
GPIO.cleanup()
