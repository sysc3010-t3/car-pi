import argparse
import handlers

from server import Server
from utils import MsgType, Metadata

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RC Camera Car Server.')
    parser.add_argument('port', type=int, help='port to listen on')

    args = parser.parse_args()
    PORT = args.port
    AP_HOST = '192.168.4.1'
    WLAN_HOST = ''

    metadata = Metadata()

    # Access point functionality that only handles returning nearby SSIDs and
    # connecting to WiFi
    server = Server(AP_HOST, PORT, metadata)
    server.add_handler(MsgType.GET_SSID, handlers.handle_get_ssid)
    server.add_handler(MsgType.WIFI_CONN, handlers.handle_connect_wifi)
    server.receive_forever()

    # Server functionality that occurs after the car connects to WiFi
    server = Server(WLAN_HOST, PORT, metadata)
    server.add_handler(MsgType.MOVE, handlers.handle_move)
    server.add_handler(MsgType.SET_LED, handlers.handle_set_led)

    carID = handlers.handle_register_car(server)
    metadata.set_car_id(carID)
    handlers.handle_connect_car(server)

    server.receive_forever()
