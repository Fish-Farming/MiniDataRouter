import sys
import smbus2 as smbus
import datetime
import time
import json
import requests

SENSORADDRESS = 0x55

#urlBase = "http://8.218.88.75:5000/api"
urlBase = "https://fishfarm.starsknights.com:5000/api"

def auth(username, password):
    uri = urlBase + "/auth/login"
    body = {"username": username, "password": password}
    res = {}
    
    try:
        res = requests.post(uri, data = body)
        return json.loads(res.text)
    except:
        print(res.status_code)
        return {"err": res.status_code}

def addRecord(sessionKey, values):
    uri = urlBase + "/sensorrecord/group"
    print("Adding record...")
    r = auth("admin01", "admin01")    
    header = {"token": sessionKey}    
    pHbody = {"sensortype":"pH value", "value": str(values["ph"]), "record":"auto", "periodid":"FP-002-001"}
    wtbody = {"sensortype":"Water temperature", "value": str(values["temp"]), "record":"auto", "periodid":"FP-002-001"}
    grouped = {"data":[] }
    grouped["data"].append(pHbody)
    grouped["data"].append(wtbody)
    #reqBody = json.dumps(grouped)
    #print(reqBody)
    #print(type(reqBody))
    #res = requests.post(uri, data = pHbody, headers = header)
    #if(res.status_code<300):
    #    print("pH Value upload successfully")
    #else:
    #    print("pH Value upload failed")

    #res = requests.post(uri, data = wtbody, headers = header)    
    #if(res.status_code<300):
    #    print("Water Temperature Value upload successfully")
    #else:
    #    print("Water Temperature Value upload failed")
    
    res = requests.post(uri, json = grouped, headers=header)
    print(res.json())
    if(res.status_code<300):
        print( "Data upload successfully")
    else:
        print( "Data upload failed. Response code: " + res.status_code )

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
                #print("Error" + msg)
                res = {}
            
            time.sleep(2)
    return 0

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("Program was stopped manually")
