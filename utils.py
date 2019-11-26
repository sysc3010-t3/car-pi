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
    Represents the metadata of the car. Stores the `user_id` and `car_id` in a
    file.
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
            self.data = {'user_id':'','car_id':''}
            with open(self.FILENAME, 'w') as f:
                json.dump(self.data, f)

    def get_user_id(self):
        return self.data['user_id']

    def set_user_id(self, userID):
        self.data['user_id'] = userID
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
