#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 5060)

while True:
    time.sleep(1)
    s.sendto('Hello'.encode(), addr)
    response, addr = s.recvfrom(1024)
    print(response.decode())