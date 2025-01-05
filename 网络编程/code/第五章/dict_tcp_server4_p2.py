#!/usr/bin/env python2
# encoding: utf-8

import io
import argparse, socket
import datetime
import threading
from sock_tools import *

def sendPacket(sock, data):
    len_str = "{:05d}".format(len(data))
    sock.sendall(len_str.encode("utf8") + data)

def recvPacket(sock):
    data = b''
    len_data = sock_readn(sock, 5)
    if (len(len_data) < 5):
        return data
    length = int(len_data.decode("utf8"))
    data = sock_readn(sock, length)
    return data

endict = dict()

def initDict():
    fp = io.open('新东方红宝书.txt', 'r', encoding='utf8')
    for line in fp:
        words = line.split('   ')
        if len(words) == 2:
            key,value = words
            endict[key] = value.replace("\n", "")
    fp.close()

def lookupWord(word):
    if word in endict:
        return "{} : {}".format(word, endict[word])
    else:
        return "找不到单词{}".format(word)

def serveClient(sc):
    while True:
        try:
            mesg = recvPacket(sc)
            if (mesg == b''):
                break

            word = mesg.decode("utf8", errors="ignore")
            if (word == "quit"):
                break
            result = lookupWord(word)
            print(word, result)
            sendPacket(sc, result.encode("utf8"))
        except Exception as e:
            print(e)
            break
    print('Closed by {}'.format(sc.getpeername()))
    sc.close()

def server(host, port):
    initDict()
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
