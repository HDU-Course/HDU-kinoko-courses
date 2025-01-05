#!/usr/bin/env python3

import argparse, socket
import datetime
import threading

def serveClient(sc):
    while True:
        try:
            data = sc.recv(1024)
            if not data:
                break
            sc.sendall(data)
        except Exception as e:
            print(e)
            break
    sc.close()

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(15)
    print('Listening at', sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print('Connected by {}'.format(sockname))
        serveClientThread = threading.Thread(target = serveClient, args=(sc,))
        serveClientThread.start()
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Echo Server')
    parser.add_argument('host', help='host or ip adress to bind')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    server(args.host, args.port)
