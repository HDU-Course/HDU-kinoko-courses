#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygeocoder import Geocoder

# 已不能正常工作 --> 高度封装的缺点
if __name__ == '__main__':
    address = 'hangzhou dianzi university'
    print(Geocoder.geocode(address)[0].coordinates)
