#!/usr/bin/env python

#Old C Code
#https://github.com/TimJung/Passageway/blob/master/pi/pi.c

#CHIP GPIO Library
#https://github.com/xtacocorex/CHIP_IO

#Style Guide
#https://google.github.io/styleguide/pyguide.html

import CHIP_IO.GPIO as GPIO
import datetime

BEAM_1 = "XIO-P0"
BEAM_2 = "XIO-P1"

def main():
    start = datetime.datetime.now()
    end = datetime.datetime.now()
    
    beam1Fall = 0;
    beam2Fall = 0;
    
    gpio_setup()
    print "GPIO is setup"
    
    while True:
        if GPIO.event_detected(BEAM_1):
            #poll to see if this is a fall
            if not GPIO.input(BEAM_1):
                print "Beam 1 Fall"
                beam1Fall = datetime.datetime.now()
                #if other beam is tripped then don't do anything
                if not GPIO.input(BEAM_2):
                    analyze_event(beam1Fall,beam2Fall)
                
        if GPIO.event_detected(BEAM_2):
            #poll to see if this is a fall
            if not GPIO.input(BEAM_2):
                beam2Fall = datetime.datetime.now()
                print "Beam 2 Fall at " + beam2Fall
                #if other beam is tripped then don't do anything
                if not GPIO.input(BEAM_1):
                    analyze_event(beam1Fall,beam2Fall)
            
def gpio_setup():
    
    GPIO.setup(BEAM_1,GPIO.IN)
    GPIO.add_event_detect(BEAM_1, GPIO.FALLING)
    #GPIO.add_event_detect(BEAM_1, GPIO.FALLING, myfuncallback)
    
    GPIO.setup(BEAM_2,GPIO.IN)
    GPIO.add_event_detect(BEAM_2, GPIO.FALLING)
    #GPIO.add_event_detect(BEAM_2, GPIO.FALLING, myfuncallback)

#python's datetime.now() performs this function completely
#def set_time():
#    return

def analyze_event(): 
    #ensure time between the two falls is reasonable
    return

#python handles this functionality completely with the > operator    
#def is_time_greater(): 
#    return

#python handles this functionality completely with - operator
#NOTE: using - operator on two datetime objects returns timedelta object
#def has_different_time_micro(): 
#    return
    
def reset_time(): 
    return

if __name__ == "__main__":
    main()