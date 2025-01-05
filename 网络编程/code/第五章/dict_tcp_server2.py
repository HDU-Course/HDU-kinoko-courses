#!/usr/bin/env python3

import argparse, socket
import datetime
import threading
from sock_tools import *

endict = dict()

def initDict():
    fp = open('新东方红宝书.txt', 'r', encoding='utf8')
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
    data_buf = b''
    while True:
        try:
            line, data_buf = sock_buf_readline(sc, data_buf)
            if not line:
                break
            # print(line, data_buf)
            line = line.rstrip(b'\r\n')
            word = line.decode("gbk", errors="ignore")
            if (word == "quit"):
                break
            result = lookupWord(word)
            print(word, result)
            sc.sendall((result+'\r\n').encode("gbk"))
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
