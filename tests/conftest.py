import pytest
import serial
import time

PORT = '/dev/cu.usbmodem14201'
stubMode = 2

@pytest.fixture(scope="session")
def ser():
    ser = serial.Serial(PORT, timeout=2)
    time.sleep(2)
    ser.write('type:mode,mode:{0:d}'.format(stubMode).encode('utf-8'))
    time.sleep(2)
    yield ser
    ser.close()
