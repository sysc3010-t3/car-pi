import logging
import argparse
import handlers
import subprocess

from server import Server
from utils import MsgType, Metadata

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RC Camera Car Server.')
    parser.add_argument('port', type=int, help='port to listen on')

    args = parser.parse_args()
    PORT = args.port
    AP_HOST = '192.168.4.1'
    WLAN_HOST = ''

    logging.basicConfig(
        filename='server.log',
        level=logging.DEBUG,
        format='%(asctime)s, msg: %(message)s, level: %(levelname)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )

    metadata = Metadata()
    connected = handlers.handle_check_connection()

    if not connected:
        logging.debug('starting access point functionality')
        # Access point functionality that only handles returning nearby SSIDs and
        # connecting to WiFi
        server = Server(AP_HOST, PORT, metadata)
        server.add_handler(MsgType.GET_SSID, handlers.handle_get_ssid)
        server.add_handler(MsgType.WIFI_CONN, handlers.handle_connect_wifi)
        server.receive_forever()
    else:
        logging.debug('stopping access point')
        # Stop access point
        subprocess.run('./shell-scripts/stop-ap.sh')

    # Server functionality that occurs after the car connects to WiFi
    server = Server(WLAN_HOST, PORT, metadata)
    server.add_handler(MsgType.MOVE, handlers.handle_move)
    server.add_handler(MsgType.SET_LED, handlers.handle_set_led)

    if metadata.get_car_id() == '':
        # Car has not been registered
        carID = handlers.handle_register_car(server)
        metadata.set_car_id(carID)

    handlers.handle_connect_car(server)

    server.receive_forever()
