import json
import socket

from utils import MsgType, Error

class Server(object):
    """
    A class that encapsulates the UDP server that will run on the
    Remote-Controlled Camera Car. This server uses a single UDP socket for all
    incoming and outgoing messages. Once started, it will indefinitely listen
    on its single socket, expecting all UDP messages to be JSON-formatted with
    a "type" which it will use to decide which registered handler to call.
    """

    BUFFER_SIZE = 0xFF

    def __init__(self, host, port, timeout=None):
        """
        Create a new UDP server that will listen forever on a single socket
        bound to the given host and port.
        """

        self.handlers = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.socket.settimeout(timeout)

    def receive(self):
        """
        Receive a new message and return the data and source address. If the
        message is JSON-formatted and has a "type" key, then it will return the
        parsed body and the source address. If not, it will send an error to the
        sender.
        """

        data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
        try:
            body = json.loads(data)
        except json.JSONDecodeError:
            print('Received invalid JSON')
            self.send(Error.json(Error.BAD_REQ, 'invalid JSON'), addr)
            return None, None
        if body['type'] not in self.handlers:
            print('Invalid message type', body)
            self.send(Error.json(Error.BAD_REQ, 'invalid message type'), addr)
            return None, None

        return body, addr

    def receive_forever(self):
        """
        Start an infinite loop that will indefinitely block on a receive until
        a new message comes in. If the message is JSON-formatted and has a
        "type" key, then the corresponding handler will be run.
        """

        while True:
            body, addr = self.receive()
            if body == None and addr == None:
                # There was an error with the received message
                continue

            try:
                self.handlers[body['type']](self, body, addr)
            except Exception as e:
                self.send(Error.json(Error.SERVER_ERR, str(e)), addr)

    def send(self, data, address):
        """
        Send a message containing the given data from the server's UDP socket
        to the given address.
        """

        self.socket.sendto(data, address)

    def add_handler(self, message_type, handler):
        """
        Register a handler function that will be called whenever a message of
        message_type is received.
        """

        self.handlers[message_type] = handler
