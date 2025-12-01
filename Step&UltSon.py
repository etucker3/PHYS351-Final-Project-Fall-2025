##Updated on and working as of November 14th

import RPi.GPIO as GPIO
from time import sleep
import pygame
import time



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
v = 343 #soS


trig_a = 17      #ultrasonic A trigger pin
echo_a = 22      #ultrasonic A echo pin

trig_b = 17      #ultrasonic B trigger pin
echo_b = 6     #ultrasonic B echo pin

pin_a = [23, 24, 25, 5]   #stepper motor pins 
led_pins = [27, 16, 26]

for pin in led_pins:
    GPIO.setup(pin,GPIO.OUT)

pwms = [GPIO.PWM(pin,100) for pin in led_pins]

for pwm in pwms:
    pwm.start(0)
for pwm in pwms:
    for dc in range (0,100,6):
        pwm.ChangeDutyCycle(100 -dc)
        sleep(0.05)
    for dc in range (100, -1, 5):
        pwm.ChangeDutyCycle(100 -dc)
        sleep(0.05)
pwm.stop()
     



for p in pin_a:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p,0)

GPIO.setup(trig_a, GPIO.OUT)
GPIO.setup(echo_a, GPIO.IN)
GPIO.setup(trig_b, GPIO.OUT)
GPIO.setup(echo_b, GPIO.IN)

##full_step = [
##    [1,0,0,1],
##    [1,0,1,0],
##    [0,1,1,0],
##    [0,1,0,1]
##]

full_step = [
    [1,0,0,1],
    [0,1,0,1],
    [0,1,1,0],
    [1,0,1,0]
]

GPIO.output(17, False)


def read_distance(trig, echo):
    GPIO.output(trig, True)
    #sleep(0.00001)
    GPIO.output(trig, False)
    start = time.time()
    for i in range(10000):
        start = time.time()
        if GPIO.input(echo) == 1:
            break
        

        
    end = time.time()
    for i in range(10000):
        end = time.time()
        if GPIO.input(echo) == 0:
            break

        
##    while GPIO.input(echo) == 0:
##        start = time.time()
##    end = time.time()
##    while GPIO.input(echo) == 1:
##        end = time.time()

    t = end - start
    distance = v*(t/2)
    #print(distance)

    return distance*100 #cm

set_counter_a = 0   
set_counter_b = 0   

system_off = True

print("wave sensor B to turn on/off, wave sensor A to switch direction.")

x = 0.2



##while True:
##
##    dist_b = read_distance(trig_b, echo_b)
##    print(f"Sensor b: {dist_b}")
##    sleep(0.1)
##    dist_a = read_distance(trig_a, echo_a)
##    print(f"Sensor a: {dist_a}")
##    sleep(0.1)
##

dist_history_a = []
dist_history_b = []

hyst = 15
distance_trigger = 8

try:
    while True:

        dist_b = read_distance(trig_b, echo_b)
        print(f"Distance b is {dist_b}")
        #sleep(0.01)
        dist_history_b.append(dist_b)
        if len(dist_history_b) > hyst:
            dist_history_b.pop(0)
       
        if len(dist_history_b) == hyst and all(d<distance_trigger for d in dist_history_b):
            dist_history_b = [] # reset the list
            set_counter_b +=1
            print(f"Set counter on/off is {set_counter_b}")
            #sleep(x)
            system_off ^= 1
            print("system off" if system_off else "system on")

        dist_a = read_distance(trig_a, echo_a)
        print(f"Distance a is {dist_a}")
        #sleep(0.01)
        dist_history_a.append(dist_a)
        if len(dist_history_a) > hyst:
            dist_history_a.pop(0)
        if len(dist_history_a) == hyst and all(d<distance_trigger for d in dist_history_a):
            dist_history_a = [] # reset the list
            print(f"Set counter direction change is {set_counter_b}")
            set_counter_a +=1
            #sleep(x)
            print("direction change")

        if system_off:
            for p in pin_a:
                GPIO.output(p,0)
                sleep(0.01)
            
            for pin in led_pins:
                GPIO.setup(pin,GPIO.OUT)

            pwms = [GPIO.PWM(pin,100) for pin in led_pins]

            for pwm in pwms:
                pwm.start(0)
            for pwm in pwms:
                for dc in range (0,100,6):
                    pwm.ChangeDutyCycle(100 -dc)
                    sleep(0.05)
                for dc in range (100, -1, 5):
                    pwm.ChangeDutyCycle(100 -dc)
                    sleep(0.05)

     
            
            
            continue


        if set_counter_a % 2 ==0:
            for i in range(0,4):
                GPIO.output(pin_a, full_step[i])
                sleep(0.01)
        else:
            for i in range(3, -1, -1):
                GPIO.output(pin_a, full_step[i])
                sleep(0.01)


        pygame.mixer.init()

        Aff1 = pygame.mixer.Sound('/home/pi/Documents/Final/Aff1.wav')
        Aff2 = pygame.mixer.Sound('/home/pi/Documents/Final/Aff2.wav')
        Aff3 = pygame.mixer.Sound('/home/pi/Documents/Final/Aff3.wav')
        Aff4 = pygame.mixer.Sound('/home/pi/Documents/Final/Aff4.wav')        
        Aff5 = pygame.mixer.Sound('/home/pi/Documents/Final/Aff5.wav')
        Aff6 = pygame.mixer.Sound('/home/pi/Documents/Final/Aff6.wav')


        remainder = set_counter_a % 6

        if remainder == 0:
            Aff1.play()
        elif remainder == 1:
            Aff2.play()
        elif remainder == 2:
            Aff3.play()
        elif remainder == 3:
            Aff4.play()
        elif remainder == 4:
            Aff5.play()
        elif remainder == 5:
            Aff6.play()

        while pygame.mixer.get_busy():
            pygame.time.delay(100)

    
            

'''


sounds = [
    pygame.mixer.Sound('/home/pi/Documents/Final/Aff1.wav'),
    pygame.mixer.Sound('/home/pi/Documents/Final/Aff2.wav'),
    pygame.mixer.Sound('/home/pi/Documents/Final/Aff3.wav'),
    pygame.mixer.Sound('/home/pi/Documents/Final/Aff4.wav'),
    pygame.mixer.Sound('/home/pi/Documents/Final/Aff5.wav'),
    pygame.mixer.Sound('/home/pi/Documents/Final/Aff6.wav')
]


index = set_counter_a % 6     
sound = sounds[index]         

playing = sound.play()
while playing.get_busy():
    pygame.time.delay(100)
'''
            



except KeyboardInterrupt:
    pass
finally:
    print('done')
    GPIO.cleanup()


    
'''
    if dist_b < 15:     #wave detect
        set_counter_b += 1
        sleep(x)     
        system_off = (set_counter_b % 2 == 1)
        print("system on" if system_off else "system off")

    if not system_off:
        for p in pin_a:
            GPIO.output(p,0)
        sleep(x)
        continue
    
    dist_a = read_distance(trig_a, echo_a)
    if dist_a < 15:     
        set_counter_a += 1
        sleep(x)     
        print("direction Change")

    if set_counter_a % 2 == 0:  
        for i in range(0,4):
            GPIO.output(pin_a, full_step[i])
            sleep(x)
    else:
        for i in range(3,0,-1):
            GPIO.output(pin_a, full_step[i])
            sleep(x)

    d = read_distance(trig_b, echo_b)
    print(d)
    sleep(0.1)



'''
