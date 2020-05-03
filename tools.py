from serial import *
import serial.tools.list_ports
import matplotlib.pyplot as plt
import time

def init():
    global portSerie
    global arduinoPort
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if ('USB' in format(desc)):
            arduinoPort = format(port)
    portSerie = Serial(port=arduinoPort,baudrate=115200)
    time.sleep(2)
    
def sortie(commande):
    portSerie.write(commande.encode())

def entree(commande):
    portSerie.write(commande.encode())
    rep = portSerie.readline()
    rep = rep[0:len(rep)-1] # sans \n
    if (b'.' in rep):
        return (float(rep))
    else:
        return (int(rep))

def close():
    portSerie.close
    
