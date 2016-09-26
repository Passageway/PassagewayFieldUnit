#!/usr/bin/env python

#Old C Code
#https://github.com/TimJung/Passageway/blob/master/pi/pi.c

#CHIP GPIO Library
#https://github.com/xtacocorex/CHIP_IO

#Style Guide
#https://google.github.io/styleguide/pyguide.html

import CHIP_IO.GPIO as GPIO
import datetime
import sched, time

BEAM_1 = "XIO-P0"
BEAM_2 = "XIO-P1"

def main():
    start = datetime.datetime.now()
    end = datetime.datetime.now()
    
    print "set up scheduler"
    s = sched.scheduler(time.time, time.sleep)
    s.enter(60, 1, alarmHandler, (s))
    print "scheduler will output in 60 seconds"
    
    beam1Fall = datetime.datetime.min;
    beam2Fall = datetime.datetime.min;
    
    gpio_setup()
    print "GPIO is setup"
    
    while True:
        if GPIO.event_detected(BEAM_1):
            #poll to see if this is a fall
            if GPIO.input(BEAM_1):
                beam1Fall = datetime.datetime.utcnow()                
#		print "Beam 1 Fall at " + beam1Fall.strftime("%Y-%m-%d %H:%M:%S")
                #if other beam is tripped then don't do anything
                if GPIO.input(BEAM_2):
		            #TODO: this may prove to be unreliable if inbetween two beams. Revisit plausibility once field testing
                    analyze_event(beam1Fall,beam2Fall)
                
        if GPIO.event_detected(BEAM_2):
            #poll to see if this is a fall
            if GPIO.input(BEAM_2):
                beam2Fall = datetime.datetime.utcnow()
#                print "Beam 2 Fall at " + beam2Fall.strftime("%Y-%m-%d %H:%M:%S")

                #if other beam is tripped then don't do anything
                if GPIO.input(BEAM_1):
                    analyze_event(beam1Fall,beam2Fall)
            
def gpio_setup():
    
    GPIO.setup(BEAM_1,GPIO.IN)
    GPIO.add_event_detect(BEAM_1, GPIO.FALLING)
    #GPIO.add_event_detect(BEAM_1, GPIO.FALLING, myfuncallback)
    
    GPIO.setup(BEAM_2,GPIO.IN)
    GPIO.add_event_detect(BEAM_2, GPIO.FALLING)
    #GPIO.add_event_detect(BEAM_2, GPIO.FALLING, myfuncallback)

def analyze_event(pBeam1Fall,pBeam2Fall): 
    #NOTE: subtracting two datetime objects returns a timedelta object
    deltaT = pBeam1Fall - pBeam2Fall
    if deltaT.total_seconds() > 0:
        print "Entry\t" + "%s"%deltaT.total_seconds()
    else:
        print "Exit\t" + "%s"%deltaT.total_seconds()
       
    return

#sched.scheduler() can be used to the same effect
#initialize the object with: s = sched.scheduler(time.time, time.sleep)
#then set just like an alarm with: s.enter(60, 1, alarmHandler, (arg1,arg2,...))
def alarmHandler(pS):
    print "Hello World"
    pS.enter(60, 1, alarmHandler, (pS))
    return
    
def reset_time(): 
    return

if __name__ == "__main__":
    main()