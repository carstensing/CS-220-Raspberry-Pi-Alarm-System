import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.OUT)   #green toggle led
GPIO.setup(19, GPIO.OUT)   #yellow toggle led
GPIO.setup(13, GPIO.OUT)   #red toggle led
GPIO.setup(17, GPIO.OUT)   #arm disarm switch led
GPIO.setup(18, GPIO.OUT)   #red alarm led
GPIO.setup(23, GPIO.OUT)   #green alarm led
GPIO.setup(24, GPIO.OUT)   #blue alarm led
GPIO.setup(25, GPIO.OUT)   #buzzer

def xband(callback):
    global xband_counter
    global time_start
    global armed
    if GPIO.input(21) == GPIO.HIGH and armed:
        print ("xband")
        if (time.time() - time_start) >= 0.6:
            time_start = time.time()
            xband_counter = 0
        else:
            xband_counter += 1
        if xband_counter == 3:
            print ("detection")
            alarm(toggle)
#END xband
        
def alarm(toggle):
    global armed
    flash_speed = 0.05
    if armed:
        print ("alarm")
        GPIO.output(18, GPIO.LOW)   #red alarm led
        GPIO.output(23, GPIO.LOW)   #green alarm led
        GPIO.output(24, GPIO.LOW)   #blue alarm led
        GPIO.output(25, GPIO.LOW)   #buzzer
        
        GPIO.output(17, GPIO.LOW)
        GPIO.remove_event_detect(21)
        armed = False
        
        if toggle == 1:
            rgb_flash(flash_speed*3)
        elif toggle == 2:
            rgb_flash(flash_speed*2)
        elif toggle == 3:
            GPIO.output(25, GPIO.HIGH)   #buzzer
            rgb_flash(flash_speed)
        else:
            print ("Error in alarm toggle")
#END alarm

def rgb_flash(speed):
    while True:
        GPIO.output(24, GPIO.LOW)   #blue alarm led
        GPIO.output(18, GPIO.LOW)   #red alarm led
        GPIO.output(23, GPIO.HIGH)   #green alarm led
        sleep(speed)
        GPIO.output(18, GPIO.LOW)   #red alarm led
        GPIO.output(23, GPIO.LOW)   #green alarm led
        GPIO.output(24, GPIO.HIGH)   #blue alarm led
        sleep(speed)
        GPIO.output(23, GPIO.LOW)   #green alarm led
        GPIO.output(24, GPIO.LOW)   #blue alarm led
        GPIO.output(18, GPIO.HIGH)   #red alarm led
        sleep(speed)
#END rgb_flash
        
def armer(callback):
    global armed
    if GPIO.input(4) == GPIO.HIGH:
        print ("arm")
        if armed == False:
            GPIO.output(17, GPIO.HIGH)
            GPIO.add_event_detect(21, GPIO.RISING, callback=xband, bouncetime=100)
        armed = True
    else:
        print ("disarm")
        if armed == True:
            GPIO.output(17, GPIO.LOW)
            GPIO.remove_event_detect(21)
        armed = False
        GPIO.output(18, GPIO.LOW)   #red alarm led
        GPIO.output(23, GPIO.LOW)   #green alarm led
        GPIO.output(24, GPIO.LOW)   #blue alarm led
        GPIO.output(25, GPIO.LOW)   #buzzer
#END armer  
        
def toggler(callback):
    global toggle
    global armed
    if not armed:
        if GPIO.input(6) == GPIO.HIGH:   
            toggle += 1
            if toggle > 3:
                toggle = 1
            toggle_led(toggle)
#END toggler

def toggle_led(toggle):
    GPIO.output(26, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
        
    if toggle == 1:
        print ("toggle green led")
        GPIO.output(26, GPIO.HIGH)
    elif toggle == 2:
        print ("toggle yellow led")
        GPIO.output(19, GPIO.HIGH)
    elif toggle == 3:
        print ("toggle red led")
        GPIO.output(13, GPIO.HIGH)
    else:
        print ("Error in toggle led")
#END toggle_led

toggle = 1
xband_counter = 0
armed = False
time_start = time.time()

GPIO.output(26, GPIO.HIGH)   #green toggle led
GPIO.output(19, GPIO.LOW)   #yellow toggle led
GPIO.output(13, GPIO.LOW)   #red toggle led
GPIO.output(17, GPIO.LOW)   #arm disarm switch led
GPIO.output(18, GPIO.LOW)   #red alarm led
GPIO.output(23, GPIO.LOW)   #green alarm led
GPIO.output(24, GPIO.LOW)   #blue alarm led
GPIO.output(25, GPIO.LOW)   #buzzer

GPIO.add_event_detect(6, GPIO.RISING, callback=toggler, bouncetime=250)
GPIO.add_event_detect(4, GPIO.RISING, callback=armer, bouncetime=250)

while True:
    pass
print ("END")


