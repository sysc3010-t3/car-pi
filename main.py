import argparse
import handlers

from server import Server
from utils import MsgType

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RC Camera Car Server.')
    parser.add_argument('port', type=int, help='port to listen on')

    args = parser.parse_args()
    PORT = args.port
    HOST = ''

    server = Server(HOST, PORT)
    server.add_handler(MsgType.GET_SSID, handlers.handle_get_ssid)
    server.add_handler(MsgType.WIFI_CONN, handlers.handle_connect_wifi)
    server.receive_forever()
