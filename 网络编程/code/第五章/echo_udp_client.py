#!/usr/bin/env python3

import argparse, socket

MAX_BYTES = 65535

def client(host, port, mesg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))
    sock.send(mesg.encode('ascii'))
    sock.settimeout(10)
    try:
        data = sock.recv(MAX_BYTES)
        print(data.decode('ascii'))
    except socket.timeout:
        print("timeout...")

    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP Daytime Client')
    parser.add_argument('host', help='server host or ip adress')
    parser.add_argument('mesg', help='mesg send to server')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    client(args.host, args.port, args.mesg)
