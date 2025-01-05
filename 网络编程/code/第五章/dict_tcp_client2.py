#!/usr/bin/env python3

import argparse, socket
import threading
import sys

BUFSIZE = 65535

def readKeyboard(sock):
    while(True):
        mesg = input('')
        mesg += '\r\n'
        sock.sendall(mesg.encode("gbk"))
        if (mesg == "quit\r\n"):
            sock.close()
            sys.exit(0)

def readFromServer(sock):
    while(True):
        try:
            mesg = sock.recv(BUFSIZE)
            print(mesg.decode("gbk"), end='')
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
