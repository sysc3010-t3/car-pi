import json
import subprocess
import time
import socket
from server import Server

from utils import MsgType, Error, Metadata, CloseServer, SerialMsg

TIMEOUT = 5
SERVER_ADDR = ('127.0.0.1', 6006) # Replace with actual server address

def handle_get_ssid(server, body, addr):
    """
    Sends nearby available networks and their protocols to a specified
    destination.

    Arguments:
    server -- instance of Server class
    body -- JSON body of UDP packet received
    addr -- source destination of received UDP packet
    """
    try:
        # Run shell script to get nearby networks
        process = subprocess.run('./shell-scripts/get-networks.sh', text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        print("get-networks.sh exited with code {0:d}: {1}"\
                .format(err.returncode, err.output))
        raise Exception("Failed to get available networks")
    except Exception as err:
        print("error running get-networks.sh: {0}".format(str(err)))
        raise Exception("Failed to get available networks")

    networks = {}
    # Output of get-networks.sh is in the following format:
    # ssid:protocol,ssid:protocol,...
    for network in process.stdout.split(','):
        networkList = network.split(":");
        if networkList[0] != '':
            if len(networkList) < 2:
                networks[networkList[0]] = ''
            else:
                networks[networkList[0]] = networkList[1]

    resp = {'type':MsgType.ACK,'networks':networks}

    server.send(json.dumps(resp).encode('utf-8'), addr)


def handle_connect_wifi(server, body, addr):
    """
    Connects to the specified network in the body.
    Raises an exception if connection fails.

    Arguments:
    server -- instance of Server class
    body -- JSON body of UDP packet received
    addr -- source destination of received UDP packet
    """
    if 'ssid' not in body or 'user_id' not in body or 'car_name' not in body:
        server.send(Error.json(Error.BAD_REQ, 'body must include "ssid" and "user_id" and "car_name" fields'), addr)
        return

    ssid = body['ssid']

    try:
        if 'password' not in body:
            argList = ['./shell-scripts/connect-wifi.sh', ssid]
        else:
            argList = ['./shell-scripts/connect-wifi.sh', ssid, body['password']]

        process = subprocess.run(argList, check=True, capture_output=True,
                text=True)
    except subprocess.CalledProcessError as err:
        print("connect-wifi.sh exited with code {1:d}: {2}"\
                .format(ssid, err.returncode, err.output))
        raise Exception("Failed to connect to {0} network".format(ssid))
    except Exception as err:
        print("error running connect-wifi.sh: {0}".format(str(err)))
        raise Exception("Failed to connect to {0} network".format(ssid))

    # Respond to client with an ACK to confirm the connection was successful.
    # Retry if client sends the WIFI_CONN message within 10 seconds to indicate
    # that the ACK message was dropped.
    server.socket.settimeout(10)
    while True:
        server.send(json.dumps({'type': MsgType.ACK}).encode('utf-8'), addr)
        try:
            body, addr = server.receive()
        except socket.timeout:
            # WIFI_CONN message was not retried therefore the ACK was received
            # successfully
            break

    server.socket.settimeout(None)

    subprocess.run('./shell-scripts/stop-ap.sh')

    # Update metadata with user ID
    server.metadata.set_user_id(body['user_id'])
    server.metadata.set_car_name(body['car_name'])

    raise CloseServer


def handle_check_connection():
    """
    Check if connected to a WiFi network. Returns True if connected and False
    if not.
    """
    try:
        subprocess.run('./shell-scripts/check_connection.sh', check=True)
    except subprocess.CalledProcessError:
        # Not connected to wifi
        return False

    return True


def handle_register_car(server):
    """
    Registers the car with the central server. Retries forever until the wanted
    ACK is received. Returns the carID received in the ACK.

    Arguments:
    server -- instance of Server class
    """
    req = {
        "type": MsgType.REG_CAR,
        "user_id": server.metadata.get_user_id(),
        "name": server.metadata.get_car_name()
    }

    # Set receive timeout to 5 seconds in case of dropped packets
    server.socket.settimeout(TIMEOUT)

    while True:
        server.send(json.dumps(req).encode('utf-8'), SERVER_ADDR)
        # Wait for a max of 5 seconds or until the ACK from the server is received
        start = time.time()
        while time.time() - start < TIMEOUT:
            try:
                body, addr = server.receive()
            except socket.timeout:
                # Receive timed out so it has been over 5 seconds
                break

            if addr == SERVER_ADDR and body['type'] == MsgType.ACK and \
                'car_id' in body:
                # Set receive timeout back to None so it waits forever
                server.socket.settimeout(None)
                return body['car_id']


def handle_connect_car(server):
    """
    Connects the car to the central server.

    Arguments:
    server -- instance of Server class
    """
    car_id = server.metadata.get_car_id()
    req = {
        "type": MsgType.CONN_CAR,
        "car_id": car_id
    }

    # Set receive timeout to 5 seconds in case of dropped packets
    server.socket.settimeout(TIMEOUT)

    while True:
        server.send(json.dumps(req).encode('utf-8'), SERVER_ADDR)
        # Wait for a max of 5 seconds or until the ACK from the server is received
        start = time.time()
        while time.time() - start < TIMEOUT:
            try:
                body, addr = server.receive()
            except socket.timeout:
                # Receive timed out so it has been over 5 seconds
                break

            if addr == SERVER_ADDR and body['type'] == MsgType.ACK:
                # Start camera stream
                server.start_stream()
                # Set receive timeout back to None so it waits forever
                server.socket.settimeout(None)
                return


def handle_move(server, body, addr):
    """
    Passes the joystick coordinates to the Arduino via the serial port.

    Arguments:
    server -- instance of Server class
    body -- JSON body of UDP packet received
    addr -- source destination of received UDP packet
    """
    if 'x' not in body or 'y' not in body:
        server.send(Error.json(Error.BAD_REQ, 'body must include "x" and "y" fields'), addr)
        return

    x = body['x']
    y = body['y']

    if x < 0 or x > 1023 or y < 0 or y > 1023 or not isinstance(x, int) or \
            not isinstance(y, int):
        server.send(Error.json(Error.BAD_REQ, \
                '"x" and "y" values must be within the range [0, 1023]'), addr)
        return

    SerialMsg.write_16_bit(server.serial, SerialMsg.MOVE, body['x'], body['y'])


def handle_set_led(server, body, addr):
    """
    Passes the new LED state to the Arduino via the serial port.

    Arguments:
    server -- instance of Server class
    body -- JSON body of UDP packet received
    addr -- source destination of received UDP packet
    """
    if 'state' not in body:
        server.send(Error.json(Error.BAD_REQ, 'missing "state" field'), addr)
        return

    state = body['state']
    if state < 0 or state > 2 or not isinstance(state, int):
        server.send(Error.json(Error.BAD_REQ, \
                '"state" must integer in range [0, 2]'), addr)
        return

    SerialMsg.write_8_bit(server.serial, SerialMsg.LED, state)

    server.send(json.dumps({'type': MsgType.ACK}).encode('utf-8'), addr)
