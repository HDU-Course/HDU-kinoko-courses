#!/usr/bin/env python3

import argparse, socket
import datetime

MAX_BYTES = 65535

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print('Listening at', sock.getsockname())

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        sock.sendto(data, address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP Daytime Server')
    parser.add_argument('host', help='host or ip adress to bind')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    server(args.host, args.port)
