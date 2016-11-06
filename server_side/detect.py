#!/usr/bin/python
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())

for p in ports:
    if "Linux" in p[1]:
        return p[0]

