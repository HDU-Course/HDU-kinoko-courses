#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import ssl
import json
from urllib.parse import quote_plus

request_text = """\
GET /maps/api/geocode/json?address={}&sensor=false&key=AIzaSyA2kD-1eTdVJoRt_7ovvFLpOGYh6fkatDE HTTP/1.1\r\n\
Host: maps.googleapis.com\r\n\
User-Agent: HDU Network Programming Class\r\n\
Connection: close\r\n\
\r\n\
"""

# request_text = """\
# GET /maps/api/place/autocomplete/json?input={}&types=address&components=country:cn&key=AIzaSyA2kD-1eTdVJoRt_7ovvFLpOGYh6fkatDE HTTP/1.1\r\n\
# Host: maps.googleapis.com\r\n\
# User-Agent: HDU Network Programming Class\r\n\
# Connection: close\r\n\
# \r\n\
# """

# GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
# Host: ditu.google.cn:80\r\n\
HOST = "maps.googleapis.com"
PORT = 443


def geocode4(address):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock = context.wrap_socket(sock, server_hostname=HOST)
    s_sock.connect((HOST, 443))
    request = request_text.format(quote_plus(address))
    s_sock.send(request.encode('ascii'))

    # sock = socket.socket()
    # sock.connect(('ditu.google.cn', 80))
    # sock.connect(('maps.googleapis.com', 443))
    # request = request_text.format(quote_plus(address))
    # sock.sendall(request.encode('ascii'))

    raw_reply = b''
    while True:
        more = s_sock.recv(4096)
        if not more:
            break
        raw_reply += more
    s_sock.close()

    reply = raw_reply.decode('utf-8')
    print('reply is ', reply)

    # file = open("ex4_recv.txt", "w")
    # file.write(reply)
    # # 关闭文件
    # file.close()

    reply_arr = reply.split("\r\n\r\n")
    json_res = json.loads(reply_arr[1])
    return json_res['results'][0]['geometry']['location']


if __name__ == '__main__':
    print(geocode4('hangzhou dianzi university'))
