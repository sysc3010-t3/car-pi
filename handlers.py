import json
import subprocess

from utils import MsgType, Error

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
    if 'ssid' not in body:
        server.send(Error.json(Error.BAQ_REQ, 'missing ssid'), addr)
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
