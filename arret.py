from serial import *
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("==================FERMETURE DU PORT==================")
    if ('USB' in format(desc)):
        arduinoPort = format(port)

port = Serial(port=arduinoPort,baudrate=115200)


port.close()