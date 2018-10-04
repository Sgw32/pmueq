import serial
from configparser import ConfigParser
import os
def get_data(port): #returns the path (USB number) of connected device from config file
    def get_path():
        print("USB device addresses are taken from config file")
        Parser = ConfigParser()
        path = os.path.abspath('') + '\ini_configs\config.ini'
        Parser.read(path)
        port = Parser.get('default values', 'internal pmu port')
        return port

    def transform_data(Value_1, Value_2):  # transforms real value from 2 bytes
        iValue1 = ord(Value_1)
        iValue2 = ord(Value_2)
        ans = (((iValue2 & 0x7f) << 7) | (iValue1 & 0x7f))  # mask
        return ans

    try:
        ser = serial.Serial(port=port, baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                            timeout=1)
        if(ser.isOpen()):
            print("Serial port is open")
            PackageData = []
            RawByteData = []
            while True:  # getting data from serial
                IncommingValue = ser.read(size=1)
                if (ord(IncommingValue) == 0x44):  # checking the beginning of package
                    #print("DATA BEGIN, first value was added")
                    cs = 0x44  # checksum
                    for i in range(0, 22):
                        IncommingValue = ser.read(size=1)
                        RawByteData.append(IncommingValue)
                        cs ^= ord(RawByteData[i])
                    #print("Check sum = ", cs)
                    #print("Rawdata without any delete", RawByteData)
                    if (cs == 0):
                        RawByteData.pop(21)  # delete checksum from BYTE list
                        ice_state = RawByteData.pop(12)  # delete anr remember ice_state

                        #print("ice_state = ", ice_state)
                        #print("without CS and ice_state: ", RawByteData)
                        for i in range(0, 20, 2):
                            PackageData.append(transform_data(RawByteData[i], RawByteData[i + 1]))
                        PackageData.insert(7, transform_data(ice_state, chr(0)))

                        PackageData[3] = -((PackageData[3] & 0x2000) << 1) + PackageData[
                            3]  # make signed int from unsigned
                        PackageData[4] = -((PackageData[4] & 0x2000) << 1) + PackageData[
                            4]  # charge cuurent and temperature1/2
                        PackageData[10] = -((PackageData[10] & 0x2000) << 1) + PackageData[10]
                        #print("Package Data: ", PackageData)
                    else:
                        #print("Checksum is incorrect")
                        break
                    # PackageData.clear()  # clear list each loop
                    # RawByteData.clear()
                    # print("Data was cleared")
                    break
    except:
        print("Error while reading data. Check device.")
        exit()
    finally:
        return PackageData

