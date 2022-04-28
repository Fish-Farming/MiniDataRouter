import sys
import smbus2 as smbus
import datetime
import time
import json
import requests

SENSORADDRESS = 0x55

urlBase = "http://8.218.88.75:5000/api"

def auth(username, password):
    uri = urlBase + "/auth/login"
    body = {"username": username, "password": password}
    res = {}
    try:
        res = requests.post(uri, data = body)        
        return json.loads(res.text)
    except:
        return {"err": res.status_code}

def addRecord(sessionKey, values):
    uri = urlBase + "/sensorrecord"
    r = auth("admin01", "admin01")    
    header = {"token": sessionKey}    
    pHbody = {"sensortype":"pH value", "value": values["ph"], "record":"auto", "periodid":"FP-002-001"}
    wtbody = {"sensortype":"Water temperature", "value": values["temp"], "record":"auto", "periodid":"FP-002-001"}
            
    res = requests.post(uri, data = pHbody, headers = header)
    if(res.status_code<300):
        print("pH Value upload successfully")
    else:
        print("pH Value upload failed")

    res = requests.post(uri, data = wtbody, headers = header)    
    if(res.status_code<300):
        print("Water Temperature Value upload successfully")
    else:
        print("Water Temperature Value upload failed")            
        

def main(args):
    
    I2Cbus = smbus.SMBus(1)
    with smbus.SMBus(1) as I2Cbus:
        while True:
            # Sensor return
            response=""
            try:
                data=I2Cbus.read_i2c_block_data(SENSORADDRESS, 0x00,24)                
                for c in data:
                    response+=chr(c)
                    
            except:
                print("remote I/O error")
                time.sleep(0.5)
            now = datetime.datetime.now()
            print(now)
            try:
                res = json.loads(response)
                print(res)
                # if sensor return, update to database
                # Step 1: Auth
                r = auth("admin01", "admin01")
                # Step 2: Upload Record
                addRecord(r["token"], res)
                #addRecord(res)
                # end
            except:
                print("JSON Parser Error")
                res = {}
            
            time.sleep(10)
    return 0
            
if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("Program was stopped manually")
