#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygeocoder import Geocoder

if __name__ == '__main__':
    address = 'hangzhou dianzi university'
    print(Geocoder.geocode(address)[0].formatted_address.split(' ')[0])
