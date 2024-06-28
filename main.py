# Copyright © 2024 Stefan Seyfried
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# the COPYING file for more details.

import network
import socket
from time import sleep
import machine
import secrets

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.ssid, secrets.password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

try:
    connect()
except KeyboardInterrupt:
    machine.reset()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr=('192.168.200.1', 6666)
s.sendto("<1> serial2syslog.py starting up", addr)
print("serial2syslog.py starting up")

uart0 = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
msg = b'<1> '
while True:
    r = uart0.read(1)
    if not r:
        continue
    if r == b'\r' or r == b'\n':
        if len(msg) > 4:
            s.sendto(msg, addr)
            print(msg)
        msg = b'<1> '
    else:
        msg = msg + r
