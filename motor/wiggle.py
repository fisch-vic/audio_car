import RPi.GPIO as GPIO
import time
import speed
#from adafruit_motorkit import MotorKit

#Motor Setup
#Pin Numbers
Pin1 = 12
Pin2 = 16
Pin3 = 18
Pin4 = 11
Pin5 = 13
Pin6 = 15
 #Set as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Pin1, GPIO.OUT)
GPIO.setup(Pin2, GPIO.OUT)
GPIO.setup(Pin3, GPIO.OUT)
GPIO.setup(Pin4, GPIO.OUT)
GPIO.setup(Pin5, GPIO.OUT)
GPIO.setup(Pin6, GPIO.OUT)



pwm1 = GPIO.PWM(Pin1, 100)
pwm1.start(0)
pwm2 = GPIO.PWM(Pin2, 100)
pwm2.start(0)
pwm4 = GPIO.PWM(Pin4, 100)
pwm4.start(0)
pwm5 = GPIO.PWM(Pin5, 100)
pwm5.start(0)

def forward():
    pwm2.ChangeDutyCycle(0)
    pwm1.ChangeDutyCycle(50)
    GPIO.output(Pin1, GPIO.HIGH)
    GPIO.output(Pin2, GPIO.LOW)
    GPIO.output(Pin3, GPIO.HIGH)
    pwm5.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(45)
    GPIO.output(Pin4, GPIO.HIGH)
    GPIO.output(Pin5, GPIO.LOW)
    GPIO.output(Pin6, GPIO.HIGH)
def backward():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(50)
    GPIO.output(Pin1, GPIO.LOW)
    GPIO.output(Pin2, GPIO.HIGH)
    GPIO.output(Pin3, GPIO.HIGH)
    pwm4.ChangeDutyCycle(0)
    pwm5.ChangeDutyCycle(45)
    GPIO.output(Pin4, GPIO.LOW)
    GPIO.output(Pin5, GPIO.HIGH)
    GPIO.output(Pin6, GPIO.HIGH)
def turnLeft():
    pwm1.ChangeDutyCycle(60)
    pwm2.ChangeDutyCycle(0)
    GPIO.output(Pin1, GPIO.HIGH)
    GPIO.output(Pin2, GPIO.LOW)
    GPIO.output(Pin3, GPIO.HIGH)
    pwm4.ChangeDutyCycle(0)
    pwm5.ChangeDutyCycle(60)
    GPIO.output(Pin4, GPIO.LOW)
    GPIO.output(Pin5, GPIO.HIGH)
    GPIO.output(Pin6, GPIO.HIGH)
def turnRight():
    pwm1.ChangeDutyCycle(60)
    pwm2.ChangeDutyCycle(0)
    GPIO.output(Pin1, GPIO.LOW)
    GPIO.output(Pin2, GPIO.HIGH)
    GPIO.output(Pin3, GPIO.HIGH)
    pwm4.ChangeDutyCycle(0)
    pwm5.ChangeDutyCycle(60)
    GPIO.output(Pin4, GPIO.HIGH)
    GPIO.output(Pin5, GPIO.LOW)
    GPIO.output(Pin6, GPIO.HIGH)

def stop():
    GPIO.output(Pin3, GPIO.LOW)
    GPIO.output(Pin6, GPIO.LOW)
def destroy():
    GPIO.cleanup()
def square():
    #time.sleep(5)
    print("forward")
    forward()
    time.sleep(2.5)
    print("Turn Left")
    turnLeft()
    time.sleep(1)
    print("forward")
    forward()
    time.sleep(2.5)
    print("Turn Left")
    turnLeft()
    time.sleep(1)
    #time.sleep(5)
    print("forward")
    forward()
    print(speed.calculate_speed(20))
    time.sleep(2.5)
    print("Turn Left")
    turnLeft()
    time.sleep(1)

def fig8():
    #time.sleep(5)
    forward()
    time.sleep(2)
    turnRight()
    time.sleep(2)
    forward()
    time.sleep(2)
    turnLeft()
    time.sleep(2)
    

    
