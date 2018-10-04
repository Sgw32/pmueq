import serial
import time

ser = serial.Serial(port='/dev/ttyAMA0', baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=1)


def main():

    if(ser.isOpen()):
        while True:
                ser.write(b'hello')
                time.sleep(0.5)


main()
