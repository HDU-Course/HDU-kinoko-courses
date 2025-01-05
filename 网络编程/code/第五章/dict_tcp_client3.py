#!/usr/bin/env python3

import argparse, socket
import threading
import sys
from sock_tools import *

BUFSIZE = 65535
PACKET_SIZE = 250

def sendPacket(sock, data):
    sock.sendall(data)
    sock.sendall(b' ' * (PACKET_SIZE - len(data)))

def recvPacket(sock):
    data = sock_readn(sock, PACKET_SIZE)
    if (len(data) != PACKET_SIZE):
        return b''
    data = data.rstrip()
    return data

def readKeyboard(sock):
    while(True):
        mesg = input('')
        sendPacket(sock, mesg.encode("utf8"))
        if (mesg == "quit"):
            sock.close()
            sys.exit(0)

def readFromServer(sock):
    while(True):
        try:
            mesg = recvPacket(sock)
            if (mesg == b''):
                break
            print(mesg.decode("utf8"))
        except Exception as e:
            break

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print(e)
        return 
    
    print("connected!")

    keyInputThread = threading.Thread(target = readKeyboard, args=(sock,))
    keyInputThread.start()

    netRecvThread = threading.Thread(target = readFromServer, args=(sock,))
    netRecvThread.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Echo Client')
    parser.add_argument('host', help='server host or ip adress')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    client(args.host, args.port)
