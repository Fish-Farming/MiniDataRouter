import sys
import smbus2 as smbus
import datetime
import time
import json

SENSORADDRESS = 0x55

def main(args):
    I2Cbus = smbus.SMBus(1)
    with smbus.SMBus(1) as I2Cbus:
        while True:
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
            print(json.loads(response))
            time.sleep(60)
    return 0
            
if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("Program was stopped manually")
