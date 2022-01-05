import RPi.GPIO as GPIO
from time import sleep
import time, math

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
    GPIO.output(Pin4, GPIO.HIGH)
    GPIO.output(Pin5, GPIO.LOW)
    GPIO.output(Pin6, GPIO.HIGH)


dist=0.00
kph=0
rpm=0
elapse=0
sensor=35
pulse=0
srt=time.time()

def init_GPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)

def calculate_elapse(channel):
    global pulse,srt,elapse
    pulse+=1
    elapse=time.time()-srt
    srt=time.time()

def calculate_speed(r_cm):
    global pulse, elapse, rpm, dist_km,dist,kps,kph
    if elapse != 0:
        rpm = 1/elapse*60
        circ_cm = (2*math.pi)*r_cm
        dist_km=circ_cm/100000
        kps=dist_km/elapse
        kph=kps*3600
        dist = (dist_km*pulse)*1000
        return kph

def init_interrupt():
    GPIO.add_event_detect(sensor, GPIO.FALLING, callback=calculate_elapse, bouncetime=20)

if __name__ == '__main__':
    init_GPIO()
    init_interrupt()
    while True:
        forward()
        print(calculate_speed(20))
        sleep(0.1)


