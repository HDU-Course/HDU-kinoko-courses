#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# def geocode2(address):
#     parameters = {'address': address, 'sensor': 'false'}
#     base = 'http://ditu.google.cn/maps/api/geocode/json'
#     response = requests.get(base, params=parameters)
#     answer = response.json()
#     print(answer)
#     return answer['results'][0]['geometry']['location']


def geocode2(address):
    parameters = {
        'address': address,
        'sensor': 'false',
        'key': 'AIzaSyA2kD-1eTdVJoRt_7ovvFLpOGYh6fkatDE'
    }
    base = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(base, params=parameters)
    answer = response.json()
    print(answer)
    return answer['results'][0]['geometry']['location']


if __name__ == '__main__':
    print(geocode2('杭州电子科技大学下沙校区'))
