import RPi.GPIO as GPIO
import time
from adafruit_motorkit import MotorKit
import wiggle

kit=MotorKit()
kit.motor1.throttle=0.3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)


stLast1 = GPIO.input(35)
stLast2 = GPIO.input(37)
roCnt1 = 0
roCnt2 = 0
stCnt1 = 0
stCnt2 = 0
stCntTot1 = 0
stCntTot2 = 0

circ = 207 #mm
stPerRo = 40
disPerStep = circ/stPerRo

try:
    while 1:
        stateCurrent=GPIO.input(35)
        if stateCurrent != stLast1:
            stLast1 = stateCurrent
            stCnt1 +=1
            stCntTot1 +=1
        if stCnt1 == stPerRo:
            roCnt1 += 1
            stCnt1 = 0
        dis1 = disPerStep*stCntTot1
        print("Dis 1", dis1)

        stateCur = GPIO.input(37)
        if stateCur != stLast2:
            stLast2 = stateCur
            stCnt2 += 1
            stCntTot2 +=1
        if stCnt2 == stPerRo:
            roCnt2 += 1
            stCnt2 = 0
        dis2 = disPerStep*stCntTot2
        print("Dis 2", dis2)

except KeyboardInterrupt: #CTRL+C
        kit.motor1.throttle=0
        GPIO.cleanup()

while True:
    wiggle.forward()
    time.sleep(5)

