#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_remote.py
# UDP client and server for talking over the network

import argparse, random, socket, sys

MAX_BYTES = 65535

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii', errors="ignore")
        print('The client at {} says {!r}'.format(address, text[8:]))
        message = '{}: Your data was {} bytes long'.format(text[0:8], len(data))
        sock.sendto(message.encode('ascii'), address)
    sock.close()

def send_reliable_data(sock, text, data_id = 0):
    str_id = "{:08d}".format(data_id)
    try_time = 0
    delay = 0.1  # seconds
    while try_time < 10:
        try_time = try_time + 1
        sock.send((str_id + text).encode('ascii'))
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
            if (len(data) > 8):
                if (data[0:8].decode('ascii', errors="ignore") == str_id):
                    print('The server says {!r}'.format(data.decode('ascii', errors="ignore")))
                    return True
                else:
                    print('data id is mismatch, data:{!r}\n'.format(data.decode('ascii', errors="ignore")))
        except socket.timeout as exc:
            delay *= 2  # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
    return False

def client(hostname, port):
    zen = ''' \
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    '''
    lines = zen.split('\n')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    data_id = random.randint(100, 65000)
    for line in lines:
        if not (send_reliable_data(sock, line, data_id)):
            break
        data_id = data_id + 1

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
