#!/usr/bin/env python

#Old C Code
#https://github.com/TimJung/Passageway/blob/master/pi/pi.c

#CHIP GPIO Library
#https://github.com/xtacocorex/CHIP_IO

#Pyrebase
#https://github.com/thisbejim/Pyrebase

#Firebase Docs
#https://firebase.google.com/docs/database/rest/start

#Style Guide
#https://google.github.io/styleguide/pyguide.html

import CHIP_IO.GPIO as GPIO
from uuid import getnode as get_mac
import pyrebase
import datetime
import threading
import sys

BEAM_1 = "XIO-P0"
BEAM_2 = "XIO-P1"
SENDFREQ = 20
MAXTHRESH = 1
MINTHRESH = .01

entry_count = 0
exit_count = 0
db = None
mac = None

def main():
    #initialize beam falls
    beam1Fall = datetime.datetime.min;
    beam2Fall = datetime.datetime.min;
    
    firebase = firebase_setup()
    global db
    db = firebase.database()
    print("Firebase is setup")
    
    global mac
    mac = get_mac()
    print("MAC Address obtained")
    
    pull_data_config()
    
    gpio_setup()
    print("GPIO is setup")
    
    #send now as start of first interval
    asyncSendData(datetime.datetime.now())
    print("Will output/send every " + str(SENDFREQ) + " seconds")
    
    while True:
        if GPIO.event_detected(BEAM_1):
            #poll to see if this is a fall
            if GPIO.input(BEAM_1):
                beam1Fall = datetime.datetime.utcnow()                
        	    #print "Beam 1 Fall at " + beam1Fall.strftime("%Y-%m-%d %H:%M:%S")
                #if other beam is tripped then don't do anything
                if GPIO.input(BEAM_2):
                    analyze_event(beam1Fall,beam2Fall)
                
        if GPIO.event_detected(BEAM_2):
            #poll to see if this is a fall
            if GPIO.input(BEAM_2):
                beam2Fall = datetime.datetime.utcnow()
                #print "Beam 2 Fall at " + beam2Fall.strftime("%Y-%m-%d %H:%M:%S")
                #if other beam is tripped then don't do anything
                if GPIO.input(BEAM_1):
                    analyze_event(beam1Fall,beam2Fall)
            
def gpio_setup():
    GPIO.setup(BEAM_1,GPIO.IN)
    GPIO.add_event_detect(BEAM_1, GPIO.FALLING)
    GPIO.setup(BEAM_2,GPIO.IN)
    GPIO.add_event_detect(BEAM_2, GPIO.FALLING)
    
def firebase_setup():
    txt = open("apiKey.txt")
    config = {
        "apiKey": txt.read(),
        "authDomain": "project-8002914138129972242.firebaseapp.com",
        "databaseURL": "https://project-8002914138129972242.firebaseio.com",
        "storageBucket": "gs://project-8002914138129972242.appspot.com",
        "serviceAccount": "serviceCredentials.json"
    }
    return pyrebase.initialize_app(config)
    
def pull_data_config():
    global db
    units = db.child("users").get()
    print(users.val()) # {"": {"name": "EOS"}}

def analyze_event(pBeam1Fall,pBeam2Fall): 
    global entry_count, exit_count
    #NOTE: subtracting two datetime objects returns a timedelta object
    deltaT = pBeam1Fall - pBeam2Fall
    #threshold check
    if abs(deltaT.total_seconds()) > MAXTHRESH or abs(deltaT.total_seconds()) < MINTHRESH:
        print("Timing threshold broke:\t" + "%s"%deltaT.total_seconds())
        return
    if deltaT.total_seconds() > 0:
        print("Entry:\t" + "%s"%deltaT.total_seconds())
        entry_count += 1
    else:
        print("Exit:\t" + "%s"%deltaT.total_seconds())
        exit_count += 1

def asyncSendData(pStart):
    global entry_count, exit_count, db, mac
    print("Entries: " + str(entry_count) + "   Exits: " + str(exit_count))
    #set end and start times
    end = datetime.datetime.now()
    start = pStart
    #setup data json and push
    data = {"start": str(start),
            "end": str(end),
            "entry": entry_count,
            "exit": exit_count,
            "pid": mac}
    db.child("Data").push(data)
    #reset counts
    entry_count = exit_count = 0
    # call asyncSendData() again in SENDFREQ seconds
    threading.Timer(SENDFREQ, asyncSendData,[end]).start()

if __name__ == "__main__":
    main()
