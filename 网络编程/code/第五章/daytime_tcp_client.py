#!/usr/bin/env python3

import argparse, socket

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    while (True):
        reply = sock.recv(1024)
        if (reply == b''):
            break
        print(reply.decode('ascii'), end='')

    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Daytime Client')
    parser.add_argument('host', help='server host or ip adress')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    client(args.host, args.port)
