import RPi.GPIO as GPIO
import time
import random
import statistics as stat
import os
import sys

class audioCar:
    def __init__(self):
        # function to initialize car
        # GPIO uses BCM number
        GPIO.setmode(GPIO.BCM)

        # hbridge pin definitions:

        self.hbridge = {"1A":18,"2A":27,"3A":23,"4A":22}
        self.encoder = {"left":4, "right":17}
        self.led = {"a":19, "b":20, "c":21}
        self.td = 0.1
        self.encoder_time = {"4":0, "17":0}
        self.time_diff = {"4":0, "17":0}
        self.rpm = {"4":0, "17":0}
        self.speed = {"4":0, "17":0} 

        self.max_pwm = 70
        self.min_pwm = 30

        self.max_rpm = 49
        self.min_rpm = 34

        self.rpm_log = {"4":[], "17":[]} 

        self.k1 = 0
        self.k2 = 1
        self.k3 = 0

        

        # hbridge GPIO init
        for pin in self.hbridge:
            # set as ouptut
            GPIO.setup(self.hbridge[pin], GPIO.OUT)
            # set low
            GPIO.output(self.hbridge[pin], GPIO.LOW)

        self.h1A = GPIO.PWM(self.hbridge["1A"],120)
        self.h2A = GPIO.PWM(self.hbridge["2A"],120)
        self.h3A = GPIO.PWM(self.hbridge["3A"],120)
        self.h4A = GPIO.PWM(self.hbridge["4A"],120)

        self.h1A.start(0)
        self.h2A.start(0)
        self.h3A.start(0)
        self.h4A.start(0)

        self.pwm = {"4":50, "17":50} 


        # encoder init
        for pin in self.encoder:
            # set as input
            GPIO.setup(self.encoder[pin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.encoder[pin], GPIO.RISING, callback=self.encoder_callback,bouncetime=10)
    

        # led init 
        for pin in self.led:
            GPIO.setup(self.led[pin], GPIO.OUT)
            GPIO.output(self.led[pin], GPIO.HIGH)
            time.sleep(self.td)
            GPIO.output(self.led[pin], GPIO.LOW)

    def wheel(self,rpm_l,rpm_r):
        if abs(rpm_l) > self.max_rpm or abs(rpm_r) > self.max_rpm:
            print("request exceeds maximum rpm")
        elif abs(rpm_l) < self.min_rpm and rpm_l != 0 or abs(rpm_r) < self.min_rpm and rpm_r != 0:
            print("request is too slow")
        else:
            pwm_l = (abs(rpm_l) - 16.566) / 0.53929
            pwm_r = (abs(rpm_r) - 21.012) / 0.39565 

            if pwm_l < 0: pwm_l = 0
            if pwm_r < 0: pwm_r = 0

            if rpm_l >= 0:
                self.h1A.ChangeDutyCycle(pwm_l)
                self.h2A.ChangeDutyCycle(0)
            elif rpm_l <= 0:
                self.h2A.ChangeDutyCycle(pwm_l)
                self.h1A.ChangeDutyCycle(0)
            if rpm_r >= 0:
                self.h3A.ChangeDutyCycle(pwm_r)
                self.h4A.ChangeDutyCycle(0)
            elif rpm_r <= 0:
                self.h4A.ChangeDutyCycle(pwm_r)
                self.h3A.ChangeDutyCycle(0)
            
    def exit(self):
        # function to exit
        self.h1A.stop()
        self.h2A.stop()
        self.h3A.stop()
        self.h4A.stop()
        GPIO.cleanup()


    def hbridge_test(self):
        # test sequence for hbridge
        for pin in self.hbridge:
            print(pin)
            GPIO.output(self.hbridge[pin], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.hbridge[pin], GPIO.LOW)
            time.sleep(self.td)

    def encoder_callback(self,enc):
        self.time_diff[str(enc)]= time.time() - self.encoder_time[str(enc)]
        self.encoder_time[str(enc)] = time.time()
        self.rpm[str(enc)] = (60/(self.time_diff[str(enc)]*20))
        self.rpm_log[str(enc)].append(self.rpm[str(enc)])
   #     print("encoder: " + str(enc) + " rpm: " + str(self.rpm[str(enc)]) + ",  " + str(self.pwm[str(enc)]))

    def feedback_stats(self):

        l = self.rpm_log["4"]
        r = self.rpm_log["17"]

        self.lmean = stat.mean(l)
        self.rmean = stat.mean(r)

        self.lstd = stat.stdev(l)
        self.rstd = stat.stdev(r)

        
        print("Left(4): mean: " + str(self.lmean) + " standard deviation: " + str(self.lstd))
        print("Right(17): mean: " + str(self.rmean) + " standard deviation: " + str(self.rstd))

    def rando_opto(self):
        for i in range(100):
            self.rpm_log = {"4":[], "17":[]} 
            #self.k1 = random.randrange(-500,500) / 500 
            #self.k2 = 2 * random.random() - 0.2
            #self.k3 = random.randrange(-500,500) / 500 
            print("k1 = " + str(self.k1) + " k2 = " + str(self.k2) + " k3 = " + str(self.k3))
            self.motor_test()
            self.feedback_stats()


            text = ("k1 = " + str(self.k1) + " k2 = " + str(self.k2) + " k3 = " + str(self.k3) + " Left(4)- mean: " + str(self.lmean) + " standard deviation: " + str(self.lstd) + " Right(17)- mean: " + str(self.rmean) + " standard deviation: " + str(self.rstd) + " quality = " + str(round(1/((self.speed["4"]-self.lmean)*self.lstd) * 1000/((self.speed["17"]-self.rmean)*self.rstd),4)) + '\n')

            f = open("rando_opto.txt", "a")
            f.write(text)
            f.close()


    def motor_test(self):

        for i in range(1):

            speed = 49 


            self.wheel(speed,0)

            time.sleep(2)
            self.wheel(0, speed)
            time.sleep(30)

            self.wheel(0,0)


    def calibrate(self):

        mean4 = []
        mean17 = []
        median4 = []
        median17 = []
        pwm_log = []

        for pwm in range(99):
            self.rpm_log = {"4":[], "17":[]} 
            self.h1A.ChangeDutyCycle(100 - pwm)
            self.h3A.ChangeDutyCycle(100 - pwm)
            time.sleep(10)
            pwm_log.append(100-pwm)

            try: 
                mean4.append(stat.mean(self.rpm_log["4"]))
                mean17.append( stat.mean(self.rpm_log["17"]))

                median4.append(stat.median(self.rpm_log["4"]))
                median17.append(stat.median(self.rpm_log["17"]))

                
            except:
                mean4.append(0)
                mean17.append(0)
                median4.append(0)
                median17.append(0)

            self.h1A.ChangeDutyCycle(0)
            self.h3A.ChangeDutyCycle(0)
            time.sleep(10)


        f = open("calibration_data.txt", "w")
        f.write(str(median4) + "\n\n" + str(median17) + "\n\n" + str(pwm_log))
        f.close()
        print("calibration data written")





ac = audioCar()
ac.calibrate()
ac.exit()







