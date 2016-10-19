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
MINTHRESH = 0.01
RISETHRESH = .5

entry_count = 0
exit_count = 0
direction = None
db = None
mac = None

def main():
    #initialize beam falls
    beam1Rise = datetime.datetime.min;
    beam2Rise = datetime.datetime.min;
    
    firebase = firebase_setup()
    global db
    db = firebase.database()
    print("Firebase is setup")
    
    global mac
    mac = hex(get_mac())
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
            if not GPIO.input(BEAM_1) and (datetime.datetime.utcnow() - beam1Rise).total_seconds() > RISETHRESH:
                beam1Rise = datetime.datetime.utcnow()
                #print ("-----Beam 1 Rise")
                #if other beam is tripped then don't do anything
                if not GPIO.input(BEAM_2):
                    analyze_event(beam1Rise,beam2Rise)
                
        if GPIO.event_detected(BEAM_2):
            #poll to see if this is a fall
            if not GPIO.input(BEAM_2) and (datetime.datetime.utcnow() - beam2Rise).total_seconds() > RISETHRESH:
                beam2Rise = datetime.datetime.utcnow()
                #print ("-----Beam 2 Rise")
                #if other beam is tripped then don't do anything
                if not GPIO.input(BEAM_1):
                    analyze_event(beam1Rise,beam2Rise)
            
def gpio_setup():
    GPIO.setup(BEAM_1,GPIO.IN)
    GPIO.add_event_detect(BEAM_1, GPIO.RISING)
    GPIO.setup(BEAM_2,GPIO.IN)
    GPIO.add_event_detect(BEAM_2, GPIO.RISING)
    
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
    global db, direction
    found = False
    
    units = db.child("units").get()
    for unit in units.each():
        dict = unit.val()
        if (dict['cid'] == mac):
            print("We found our unit: " + str(dict['cid']))
            direction = dict['direction']
            found = True
            break
    if not found:
        #direction defaults to 0
        direction = 0
        #set up this unit on firebase
        data = {"building": "temp",
            "cid": mac,
            "direction": 0,
            "floor": 1,
            "lat": 0,
            "lon": 0,
            "name": "temp",
            "wing": "temp"}
        #push to firebase
        db.child("units").push(data)
        print("Unit not found. Pushing new unit: " + str(mac))

def analyze_event(pBeam1Rise,pBeam2Rise): 
    global entry_count, exit_count
    #NOTE: subtracting two datetime objects returns a timedelta object
    deltaT = pBeam1Rise - pBeam2Rise
    #threshold check
    if abs(deltaT.total_seconds()) > MAXTHRESH or abs(deltaT.total_seconds()) < MINTHRESH:
        print("Timing threshold broke:\t" + "%s"%deltaT.total_seconds())
        return
    if direction == 0:
        if deltaT.total_seconds() > 0:
            print("Entry:\t" + "%s"%deltaT.total_seconds())
            entry_count += 1
        else:
            print("Exit:\t" + "%s"%deltaT.total_seconds())
            exit_count += 1
    elif direction == 1:
        if deltaT.total_seconds() < 0:
            print("Entry:\t" + "%s"%deltaT.total_seconds())
            entry_count += 1
        else:
            print("Exit:\t" + "%s"%deltaT.total_seconds())
            exit_count += 1
    else:
        print("Direction not correctly configured")
        quit()

def asyncSendData(pStart):
    global entry_count, exit_count, db, mac
    end = datetime.datetime.now()
    if entry_count != 0 or exit_count != 0:
        print("Entries: " + str(entry_count) + "   Exits: " + str(exit_count))
        #set end and start times
        start = pStart
        #setup data json
        data = {"start": str(start),
                "end": str(end),
                "entry": entry_count,
                "exit": exit_count,
                "cid": mac}
        #push to firebase
        db.child("data").push(data)
        #reset counts
        #entry_count = exit_count = 0
    # call asyncSendData() again in SENDFREQ seconds
    threading.Timer(SENDFREQ, asyncSendData,[end]).start()

if __name__ == "__main__":
    main()
