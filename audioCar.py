import RPi.GPIO as GPIO
import time
import random
import statistics as stat

class audioCar:
    def __init__(self):
        # function to initialize car
        # GPIO uses pin number
        GPIO.setmode(GPIO.BCM)

        # hbridge pin definitions:

        self.hbridge = {"1A":18,"2A":27,"3A":22,"4A":23}
        self.encoder = {"left":4, "right":17}
        self.led = {"a":19, "b":20, "c":21}
        self.td = 0.1
        self.encoder_time = {"4":0, "17":0}
        self.time_diff = {"4":0, "17":0}
        self.rpm = {"4":0, "17":0}
        self.speed = {"4":0, "17":0} 

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

        self.h1A = GPIO.PWM(self.hbridge["1A"],60)
        self.h2A = GPIO.PWM(self.hbridge["2A"],60)
        self.h3A = GPIO.PWM(self.hbridge["3A"],60)
        self.h4A = GPIO.PWM(self.hbridge["4A"],60)

        self.h1A.start(0)
        self.h2A.start(0)
        self.h3A.start(0)
        self.h4A.start(0)

        self.pwm = {"4":50, "17":50} 


        # encoder init
        for pin in self.encoder:
            # set as input
            GPIO.setup(self.encoder[pin], GPIO.IN)
            GPIO.add_event_detect(self.encoder[pin], GPIO.FALLING, callback=self.encoder_callback,bouncetime=50)
    

        # led init 
        for pin in self.led:
            GPIO.setup(self.led[pin], GPIO.OUT)
            GPIO.output(self.led[pin], GPIO.HIGH)
            time.sleep(self.td)
            GPIO.output(self.led[pin], GPIO.LOW)


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


    def ignore(self):
        diff = (abs(self.speed[str(enc)])- self.rpm[str(enc)])
        self.pwm[str(enc)] += diff*self.k2
        if self.pwm[str(enc)] > 100:
            self.pwm[str(enc)] = 100
        # don't stall out
        if self.pwm[str(enc)] < 20:
            self.pwm[str(enc)] = 20
        # but still stop
        if self.speed[str(enc)] == 0: 
            self.pwm[str(enc)] = 0

        if enc == 4 and self.speed[str(enc)] >= 0:
            self.h1A.ChangeDutyCycle(int(self.pwm[str(enc)]))
            self.h2A.ChangeDutyCycle(0)
        elif enc == 4 and self.speed[str(enc)] <= 0:
            self.h2A.ChangeDutyCycle(int(self.pwm[str(enc)]))
            self.h1A.ChangeDutyCycle(0)
        elif enc == 17 and self.speed[str(enc)] >= 0:
            self.h3A.ChangeDutyCycle(int(self.pwm[str(enc)]))
            self.h4A.ChangeDutyCycle(0)
        elif enc == 17 and self.speed[str(enc)] <= 0:
            self.h4A.ChangeDutyCycle(int(self.pwm[str(enc)]))
            self.h3A.ChangeDutyCycle(0)
 
 
        print("encoder: " + str(enc) + " rpm: " + str(self.rpm[str(enc)]) + ",  " + str(self.pwm[str(enc)]))

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

        for i in range(10):

            self.pwm = {"4":50, "17":50} 
            self.speed["4"] = 40 
            self.speed["17"] = 40
            self.h1A.ChangeDutyCycle(100)
            self.h3A.ChangeDutyCycle(100)
            time.sleep(1)
            
            self.speed["4"] = 0 
            self.speed["17"] = 0 
            time.sleep(1)


            self.pwm = {"4":50, "17":50} 
            self.speed["4"] = -40 
            self.speed["17"] = -40 
            self.h2A.ChangeDutyCycle(100)
            self.h4A.ChangeDutyCycle(100)
            time.sleep(1)

            self.speed["4"] = 0 
            self.speed["17"] = 0 
            time.sleep(1)

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

        f = open("calibration_data.txt", "w")
        f.write(str(median4) + "\n\n" + str(median17) + "\n\n" + str(pwm_log))
        f.close()
        print("calibration data written")





ac = audioCar()
ac.calibrate()
ac.exit()







