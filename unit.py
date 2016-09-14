#!/usr/bin/env python

#Old C Code
#https://github.com/TimJung/Passageway/blob/master/pi/pi.c

#CHIP GPIO Library
#https://github.com/xtacocorex/CHIP_IO

import CHIP_IO.GPIO as GPIO

BEAM_1 = "XIO-P0"
BEAM_2 = "XIO-P6"

def main():
    
    gpio_setup()
    print "GPIO is setup"
    
    while True:
        if GPIO.event_detected(BEAM_1):
            print "Beam 1 Fall"
        if GPIO.event_detected(BEAM_2):
            print "Beam 2 Fall"
    
def gpio_setup():
    GPIO.setup(BEAM_1,GPIO.IN)
    GPIO.add_event_detect(BEAM_1, GPIO.FALLING)
    GPIO.setup(BEAM_2,GPIO.IN)
    GPIO.add_event_detect(BEAM_2, GPIO.FALLING)

def set_time():
    return

def analyze_event(): 
    return
    
def is_time_greater(): 
    return
    
def has_different_time_micro(): 
    return
    
def reset_time(): 
    return

if __name__ == "__main__":
    main()