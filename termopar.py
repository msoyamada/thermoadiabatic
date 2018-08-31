#!/usr/bin/python

#   return 1/(1/self.T0 + (1/self.B) * np.log(R/self.R0)) - (273.15)
import mraa
import time
import numpy as np
import dweepy
import os
import datetime
import sys
import csv


import netifaces


#time.sleep(120)

ifaces=''

def getifaces():
	global ifaces
	ifaces= ''
	interfaces = netifaces.interfaces()
	for i in interfaces:
    		if i == 'lo':
        		continue
    		iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
    		if iface != None:
        		for j in iface:
            			ifaces +=  j['addr']

def readCelsius(CS):
   CS.write(0)
   esc=spi.writeByte(0x00) #First byte with input info
   esc2=spi.writeByte(0x00) #Complete the 16bits --> Clock
   CS.write(1) #CS=1 <--- Disables the device

   v= (esc << 8) | esc2
   if (v & 0x4):
     return float('nan')
   v >>= 3
   return v*0.25




# inicia o controle geral 
spi=mraa.Spi(0) #Bus comunication
spi.mode(mraa.SPI_MODE0) #Comunication MODE0
spi.frequency(2000000) #Frequency of 2MHz
spi.lsbmode(False) #Format data MSB

# first termopar
ss1=mraa.Gpio(4)
ss1.dir(mraa.DIR_OUT)
ss1.write(1)

#second termopar
ss2= mraa.Gpio(5)
ss2.dir(mraa.DIR_OUT)
ss2.write(1)


#second termopar
ss3= mraa.Gpio(6)
ss3.dir(mraa.DIR_OUT)
ss3.write(1)


#second termopar
ss4= mraa.Gpio(7)
ss4.dir(mraa.DIR_OUT)
ss4.write(1)



while 1:
    Rx  = readCelsius(ss1)
    print (Rx)
    Rx  = readCelsius(ss2)
    print (Rx)
    Rx  = readCelsius(ss3)
    print (Rx)

    Rx  = readCelsius(ss4)
    print (Rx)

    time.sleep(2)

