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

        self.revs = {"4":0, "17":0} 

        self.max_pwm = 70
        self.min_pwm = 30

        self.max_rpm = 120 
        self.min_rpm = 55 

        self.rpm_log = {"4":[], "17":[]} 

        self.wdia = 2.625
        self.wcir = 3.14159 * self.wdia
        

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
        # start rolling at a specific rpm

        pwm_l = (abs(rpm_l) - 39.984) / 0.84904
        pwm_r = (abs(rpm_r) - 32.57) / 0.93539 

        if pwm_l < 0: pwm_l = 0
        if pwm_r < 0: pwm_r = 0
        if pwm_l > 100: pwm_l = 100
        if pwm_r > 100: pwm_r = 100

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
        # encoder call back
        # calc time differnece between pulces
        self.time_diff[str(enc)]= time.time() - self.encoder_time[str(enc)]
        # reset time for next calculation
        self.encoder_time[str(enc)] = time.time()
        # calculate & record rpm 
        self.rpm[str(enc)] = (60/(self.time_diff[str(enc)]*20))
        self.rpm_log[str(enc)].append(self.rpm[str(enc)])
        # tally revolution
        self.revs[str(enc)] += 1/20
#        print("encoder: " + str(enc) + " rpm: " + str(self.rpm[str(enc)]) + ",  " + str(self.pwm[str(enc)]) + " " + str(self.revs[str(enc)]))

    def feedback_stats(self):
        # calculate rpm stats

        l = self.rpm_log["4"]
        r = self.rpm_log["17"]

        self.lmean = stat.mean(l)
        self.rmean = stat.mean(r)

        self.lstd = stat.stdev(l)
        self.rstd = stat.stdev(r)

        
        print("Left(4): mean: " + str(self.lmean) + " standard deviation: " + str(self.lstd))
        print("Right(17): mean: " + str(self.rmean) + " standard deviation: " + str(self.rstd))


    def motor_test(self):

        for i in range(5):

            speed = 120 


            self.wheel(speed,speed)

            time.sleep(2)
            self.wheel(-1 * speed, -1 * speed)
            time.sleep(2)

            self.wheel(0,0)

    def drive_straight(self,speed,length):
        # calculate target rev 
        target_revs = length / self.wcir
        # reset distance count
        self.revs["4"] = 0
        self.revs["17"] = 0
        # initialize modulation variable
        mod = 0

        # start rolling
        self.wheel(speed,speed)

        # try and match rate
        while(self.revs["4"] < target_revs):
            if self.revs["4"] - self.revs["17"] > .001:
                # if difference in revolution count between tires
                mod = abs(self.revs["4"] - self.revs["17"])
                self.wheel(speed,speed + mod * (speed / abs(speed)))

            if self.revs["17"] - self.revs["4"] > .001:
                mod = abs(self.revs["4"] - self.revs["17"])
                self.wheel(speed,speed + mod* (speed / abs(speed)))

            time.sleep(abs(speed) / 60 / 20)

    def drive_curve(self, radius, angle):
        min_rad = 7.5
        width = 5.5
        omega = 2 * 3.14

        l_radius = radius + width / 2
        r_radius = radius - width / 2

        l_speed = l_radius*omega
        r_speed = r_radius*omega
        
               #find arc length
        sl = angle * l_radius
        target_revsl = sl / self.wcir

        sr = angle * r_radius
        target_revsr = sr / self.wcir

        # reset distance count
        self.revs["4"] = 0
        self.revs["17"] = 0
        
        if l_speed < r_speed:
            r_speed = r_speed*self.min_rpm/l_speed
            l_speed = l_speed*self.min_rpm/l_speed

        if r_speed < l_speed:
            l_speed = l_speed*self.min_rpm/r_speed
            r_speed = r_speed*self.min_rpm/r_speed

        print(l_speed)
        print(r_speed)
 
        self.wheel(100,100)
        time.sleep(0.02)
        self.wheel(l_speed,r_speed)
        calc_theta = 0

        
        while(calc_theta < angle):
            calc_theta = (abs(self.revs["4"] - self.revs["17"]))*self.wcir / width
            print(calc_theta)
        self.wheel(0, 0)


    def figure_line(self):
        # drive in straight line of length inches
        length = 36 
        speed = 100

        print("driving " + str(length) + " inch straight lines ")

        self.drive_straight(speed,length)
        self.drive_straight(-speed,length)

    def figure_8(self):
        length = 36
        speed = 100
        for i in range(2):
            self.drive_straight(speed,length)
            self.wheel(120,60)
            time.sleep(3)
            self.wheel(0,0)
            self.drive_straight(speed,length)
            self.wheel(65,100)
            time.sleep(3)
            self.wheel(0,0)
        #doesn't work, wheels aren't remotely consistant.
 

    def calibrate(self):

        mean4 = []
        mean17 = []
        median4 = []
        median17 = []
        pwm_log = []

        for pwm in range(20):
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
#ac.figure_line()
ac.figure_8()
ac.exit()


