import serial
import time

def test_joystick_forward(ser):
    ser.write('type:move,xaxis:550,yaxis:1023'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=1'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=0'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=1'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=0'

def test_joystick_backward(ser):
    ser.write('type:move,xaxis:550,yaxis:0'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=0'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=255'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=0'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=255'

def test_joystick_left(ser):
    ser.write('type:move,xaxis:0,yaxis:550'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=1'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=255'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=1'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=0'

def test_joystick_right(ser):
    ser.write('type:move,xaxis:1023,yaxis:550'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=1'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=0'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=1'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=255'

def test_joystick_forward_left(ser):
    ser.write('type:move,xaxis:0,yaxis:1023'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=1'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=255'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=1'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=0'

def test_joystick_forward_right(ser):
    ser.write('type:move,xaxis:1023,yaxis:1023'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=1'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=0'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=1'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=255'

def test_joystick_backward_left(ser):
    ser.write('type:move,xaxis:0,yaxis:0'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=0'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=0'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=0'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=255'

def test_joystick_backward_right(ser):
    ser.write('type:move,xaxis:1023,yaxis:0'.encode('utf-8'))

    dirL = ser.readline()
    assert dirL.decode('utf-8').rstrip() == 'dir_L=0'

    speedL = ser.readline()
    assert speedL.decode('utf-8').rstrip() == 'speed_L=255'

    dirR = ser.readline()
    assert dirR.decode('utf-8').rstrip() == 'dir_R=0'

    speedR = ser.readline()
    assert speedR.decode('utf-8').rstrip() == 'speed_R=0'
