import socket
import fcntl
import struct
import pyrebase
from uuid import getnode as get_mac

db = None
mac = None
ip = None

def main():
    
    global ip
    ip = get_ip_address("wlan0")
    print("IP Address obtained: " + ip)
    
    global mac
    mac = hex(get_mac())
    print("MAC Address obtained")
    
    firebase = firebase_setup()
    global db
    db = firebase.database()
    print("Firebase is setup")
    
    update_ip()
  
def update_ip():    
    found = False

    units = db.child("units").get()
    for unit in units.each():
        dict = unit.val()
        if (dict['cid'] == mac):
            #update firebase entry
            #data = unit.val()
            data = {"ip": ip}
            db.child("units").child(unit.key()).update(data)
            found = True
            print("We found our unit: " + str(dict['cid']) + " Updating IP Address")
            break
    if not found:
        #push to firebase
        data = {"building": "temp",
            "ip": ip,
            "cid": mac,
            "direction": 0,
            "floor": 1,
            "lat": 0,
            "lon": 0,
            "name": "temp",
            "wing": "temp"}
        db.child("units").push(data)
        print("Unit not found. Pushing new unit: " + str(mac))
 
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

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s',ifname[:15].encode('utf-8'))
    )[20:24])
    
if __name__ == "__main__":
    main()

