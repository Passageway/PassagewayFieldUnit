#!/usr/bin/env python

#Old C Code
#https://github.com/TimJung/Passageway/blob/master/pi/pi.c

#CHIP GPIO Library
#https://github.com/xtacocorex/CHIP_IO

#Style Guide
#https://google.github.io/styleguide/pyguide.html

import CHIP_IO.GPIO as GPIO
import datetime
import threading

BEAM_1 = "XIO-P0"
BEAM_2 = "XIO-P1"
SENDFREQ = 6
MAXTHRESH = 1
MINTHRESH = .01

entry_count = 0
exit_count = 0

def main():
    start = datetime.datetime.now()
    end = datetime.datetime.now()
    
    print "set up data send"
    asyncSendData()
    print "will output every " + str(SENDFREQ) + " seconds"
    
    beam1Fall = datetime.datetime.min;
    beam2Fall = datetime.datetime.min;
    
    gpio_setup()
    print "GPIO is setup"
    
    while True:
        if GPIO.event_detected(BEAM_1):
            #poll to see if this is a fall
            if GPIO.input(BEAM_1):
                beam1Fall = datetime.datetime.utcnow()                
        	print "Beam 1 Fall at " + beam1Fall.strftime("%Y-%m-%d %H:%M:%S")
                #if other beam is tripped then don't do anything
                if GPIO.input(BEAM_2):
                    analyze_event(beam1Fall,beam2Fall)
                
        if GPIO.event_detected(BEAM_2):
            #poll to see if this is a fall
            if GPIO.input(BEAM_2):
                beam2Fall = datetime.datetime.utcnow()
                print "Beam 2 Fall at " + beam2Fall.strftime("%Y-%m-%d %H:%M:%S")
                #if other beam is tripped then don't do anything
                if GPIO.input(BEAM_1):
                    analyze_event(beam1Fall,beam2Fall)
            
def gpio_setup():
    
    GPIO.setup(BEAM_1,GPIO.IN)
    GPIO.add_event_detect(BEAM_1, GPIO.FALLING)
    
    GPIO.setup(BEAM_2,GPIO.IN)
    GPIO.add_event_detect(BEAM_2, GPIO.FALLING)

def analyze_event(pBeam1Fall,pBeam2Fall): 
    global entry_count, exit_count
    #NOTE: subtracting two datetime objects returns a timedelta object
    deltaT = pBeam1Fall - pBeam2Fall
    #threshold check
    if abs(deltaT.total_seconds()) > MAXTHRESH or abs(deltaT.total_seconds()) < MINTHRESH:
        print "threshold broke, mofo" + "%s"%deltaT.total_seconds()
	return
    if deltaT.total_seconds() > 0:
        print "Entry\t" + "%s"%deltaT.total_seconds()
        entry_count += 1
    else:
        print "Exit\t" + "%s"%deltaT.total_seconds()
        exit_count += 1
    return

def asyncSendData():
    global entry_count, exit_count
    print "Entries: " + str(entry_count) + "   Exits: " + str(exit_count)
    
    #entry_count = exit_count = 0

    # call asyncSendData() again in SENDFREQ seconds
    threading.Timer(SENDFREQ, asyncSendData).start()

if __name__ == "__main__":
    main()
