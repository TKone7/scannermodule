#!/usr/bin/env python
import time
import serial
import datetime

def encode(cmd):
    return cmd.encode('ascii')+bytes([13, 10])

ser = serial.Serial(
 port='/dev/ttyUSB0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0
scantimeout=10
CONTMODE = '~M00210001.'
INDMODE = '~M00210002.'
CMDMODE = '~M00210003.'
mode = CMDMODE

# setup 
ser.write(encode('~M00910001.'))
print(ser.readline())

# define mode
ser.write(encode(mode))
print(ser.readline())

# turn off sleep
# ser.write(encode('~M00220000'))
# print(ser.readline())

# store settings and exit setup mode
ser.write(encode('~MA5F0506A.'))
print(ser.readline())
ser.write(encode('~M00910000.'))
print(ser.readline())

def activate_scanner():
    ser.write(encode('~T.'))
    time.sleep(0.1)
    res = ser.readline()
    if res == b'T\x06':
        return True
    else:
        return False

while 1:
    input("Press Enter to scan...")
    if activate_scanner():
        code = None
        start_time = datetime.datetime.now()
        passed = start_time - start_time
        while not code and passed < datetime.timedelta(seconds=scantimeout):
            code = ser.readline()
            passed = datetime.datetime.now() - start_time
        print(code)
