#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import http.client
import json
from urllib.parse import quote_plus

# base = '/maps/api/geocode/json'
# def geocode3(address):
#     path = '{}?address={}&sensor=false'.format(base, quote_plus(address))
#     connection = http.client.HTTPConnection('ditu.google.cn')
#     connection.request('GET', path)
#     rawreply = connection.getresponse().read()
#     reply = json.loads(rawreply.decode('utf-8'))
#     return reply['results'][0]['geometry']['location']

base = '/maps/api/geocode/json'


def geocode3(address):
    path = '{}?address={}&sensor=false&key=AIzaSyA2kD-1eTdVJoRt_7ovvFLpOGYh6fkatDE'.format(
        base, quote_plus(address))
    connection = http.client.HTTPSConnection('maps.googleapis.com')
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    print('reply is ', reply)
    return reply['results'][0]['geometry']['location']


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        address = sys.argv[1]
    else:
        address = '杭州电子科技大学下沙校区'

    print(address, geocode3(address))
