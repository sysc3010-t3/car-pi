import json
from enum import IntEnum
from os import path

class MsgType(IntEnum):
    ACK = 0
    ERROR = 1
    LINK = 5
    REG_CAR = 6
    CONN_CAR = 7
    MOVE = 8
    GET_SSID = 9
    WIFI_CONN = 10
    SET_LED = 11

class Error(IntEnum):
    BAD_REQ = 0
    UNAUTHORIZED = 1
    SERVER_ERR = 2

    @staticmethod
    def json(errType, errMsg):
        body = { 'type': MsgType.ERROR, 'error_type': errType,
                'error_msg': errMsg }
        return json.dumps(body).encode('utf-8')

class Metadata(object):
    """
    Represents the metadata of the car. Stores the `user_id`, `car_name`, and
    `car_id` in a file.
    """

    FILENAME = 'metadata.json'

    def __init__(self):
        """
        Load existing metadata from JSON file or create new JSON file with empty
        metadata.
        """

        if path.exists(self.FILENAME):
            with open(self.FILENAME) as f:
                self.data = json.load(f)
        else:
            self.data = {'user_id':'','car_name':'','car_id':''}
            with open(self.FILENAME, 'w') as f:
                json.dump(self.data, f)

    def get_user_id(self):
        return self.data['user_id']

    def set_user_id(self, userID):
        self.data['user_id'] = userID
        with open(self.FILENAME, 'w') as f:
            json.dump(self.data, f)

    def get_car_name(self):
        return self.data['car_name']

    def set_car_name(self, carName):
        self.data['car_name'] = carName
        with open(self.FILENAME, 'w') as f:
            json.dump(self.data, f)

    def get_car_id(self):
        return self.data['car_id']

    def set_car_id(self, carID):
        self.data['car_id'] = carID
        with open(self.FILENAME, 'w') as f:
            json.dump(self.data, f)

class CloseServer(Exception):
    """
    Exception that is raised to indicate that the server should be closed.
    """
    pass

class SerialMsg(IntEnum):
    MOVE = 0
    LED = 1
    MODE = 2

    @staticmethod
    def write_16_bit(serial, msgType, val1, val2):
        """
        Writes a message to the serial port with 16-bit values instead of 8-bit.
        Raises an exception if error occurred while converting the values to
        bytes.

        Arguments:
        serial -- instance of Serial class
        msgType -- integer that represents the type of the message being sent
        val1 -- integer that will be converted to 2 bytes and sent
        val2 -- integer that will be converted to 2 bytes and sent
        """
        try:
            val1High, val1Low = val1.to_bytes(2, byteorder='big')
            val2High, val2Low = val2.to_bytes(2, byteorder='big')
        except OverflowError:
            raise Exception('unable to convert values to 16-bit words')

        data = bytes([msgType, val1High, val1Low, val2High, val2Low]) + b'\n'
        serial.write(data)

    @staticmethod
    def write_8_bit(serial, msgType, val):
        """
        Writes a message to the serial port with an 8-bit value.

        Arguments:
        serial -- instance of Serial class
        msgType -- integer that represents the type of the message being sent
        val -- integer that will be sent
        """
        serial.write(bytes([msgType, val]) + b'\n')
