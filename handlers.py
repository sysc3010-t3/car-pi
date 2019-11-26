import json
import subprocess
from server import Server

from utils import MsgType, Error

SERVER_IP = '192.168.4.19'
WLAN_IP = '192.168.0.154'
PORT = 8080

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


def register_car(userID):
    """
    Registers the car with the central server. Retries forever until the wanted
    ACK is received. Returns the carID received in the ACK.

    Arguments:
    userID -- The ID of the user that is registering the car
    """
    server = Server(WLAN_IP, PORT, 60)
    attempts = 0
    while True:
        req = {"type": MsgType.REG_CAR, "user_id": userID}
        server.send(json.dumps(req).encode('utf-8'), SERVER_IP)
        # Wait for a max of 1 minute until the ACK from the server is received
        start = time.time()
        valid = False
        while time.time() - start < 60:
            body, addr = receive()
            if addr == SERVER_IP and body['type'] == MsgType.ACK and \
                'car_id' in body:
                valid = True
                break
        if valid:
            return body['car_id']


def handle_connect_wifi(server, body, addr):
    """
    Connects to the specified network in the body.
    Raises an exception if connection fails.

    Arguments:
    server -- instance of Server class
    body -- JSON body of UDP packet received
    addr -- source destination of received UDP packet
    """
    if 'ssid' not in body or 'user_id' not in body:
        server.send(Error.json(Error.BAD_REQ, 'body must include "ssid" and "user_id" fields'), addr)
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

    # Respond to client with an ACK to confirm the connection was successful
    server.send(json.dumps({'type': MsgType.ACK}).encode('utf-8'), addr)

    subprocess.run('./shell-scripts/stop-ap.sh')

    carID = register_car(body['user_id'])
