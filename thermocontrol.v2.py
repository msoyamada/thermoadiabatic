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
relay_pin= mraa.Gpio(0)
relay_pin.dir(mraa.DIR_OUT)
relay_pin.write(1)



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








#first termopar
ss1= mraa.Gpio(4)
ss1.dir(mraa.DIR_OUT)
ss1.write(1)
#second termopar
ss2= mraa.Gpio(5)
ss2.dir(mraa.DIR_OUT)
ss2.write(1)


#third termopar
ss3= mraa.Gpio(6)
ss3.dir(mraa.DIR_OUT)
ss3.write(1)


#forth termopar
ss4= mraa.Gpio(7)
ss4.dir(mraa.DIR_OUT)
ss4.write(1)








def ReadCsvDataPoints():
	try: 
		with open('/home/root/data.csv', 'rb') as f:
    			reader = csv.reader(f, dialect= 'excel')
			l= list(reader)
		print l		
	except:
		print('error: data points not found');
		l = [['Ciclo,Tempo, Temp'], ['1; 30; 60']]
	return l



os.environ["http_proxy"]="http://marcio.oyamada:Helena3001@proxy.unioeste.br:8080"
os.environ["https_proxy"]="http://marcio.oyamada:Helena3001@proxy.unioeste.br:8080"


R0=10000
BCOEF= 3950
TEMPERATURENOMINAL =27

def Rx_to_T(R):
	global BCOEF
	R0x= 10800
	global TEMPERATURENOMINAL
	steinhart = R / R0x;     # (R/Ro)
	steinhart = np.log(steinhart);                  # ln(R/Ro)
	steinhart /= BCOEF;                   # 1/B * ln(R/Ro)
	steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); # + (1/To)
	steinhart = 1.0 / steinhart;                 # Invert
	steinhart -= 273.15;                        # convert to C
	return steinhart
def Ry_to_T(R):
	global BCOEF
	R0y= 10600
	global TEMPERATURENOMINAL
	steinhart = R / R0y;     # (R/Ro)
	steinhart = np.log(steinhart);                  # ln(R/Ro)
	steinhart /= BCOEF;                   # 1/B * ln(R/Ro)
	steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); # + (1/To)
	steinhart = 1.0 / steinhart;                 # Invert
	steinhart -= 273.15;                        # convert to C
	return steinhart
def Rz_to_T(R):
	global BCOEF
        R0z= 10600
	global TEMPERATURENOMINAL
	steinhart = R / R0z;     # (R/Ro)
	steinhart = np.log(steinhart);                  # ln(R/Ro)
	steinhart /= BCOEF;                   # 1/B * ln(R/Ro)
	steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); # + (1/To)
	steinhart = 1.0 / steinhart;                 # Invert
	steinhart -= 273.15;                        # convert to C
	return steinhart


def getTargetTemp(ciclo, l):
	target= 0;
	if (len(l) < (ciclo-1)):
		#t= l([len(l)-1])
		#ciclo, tempo,target= t[0].split(';')
		print('ciclos finalizados')
		exit()
	else:
		t= l[ciclo]
		ciclo, tempo, target= t[0].split( ';')
	return float(target)
	

l = ReadCsvDataPoints()
print l

# Arquivo que armazena em qual ciclo eele estperando, para preservar o 
#estado eno cas de queda de energia
try: 
	cicloLog= open("/www/pages/ciclo.txt", "r+");
except:
	cicloLog= open("/www/pages/ciclo.txt", "w");

	
if os.path.getsize("/www/pages/ciclo.txt") == 0 :  #se vazio inicia novo ciclo
	cicloLog.write("1")
	cicloLog.flush()
	ciclo= 1
else:
	ciclo = int(cicloLog.read())
	cicloLog.seek(0);


# Arquivo de Log geral
f= open("/www/pages/temp.txt", "a");

# inicia o controle geral 
targetTemp = getTargetTemp(ciclo,l)
print('Target temp is' , targetTemp)
x = mraa.Aio(1)
y = mraa.Aio(2)
switch1= 0

switchPIN = mraa.Gpio(13)
switchPIN.dir(mraa.DIR_OUT)
switchPIN.write(switch1)
clock_begin= time.time()
count =0;
time_begin= time.time()

#for termopar 
# inicia o controle geral
spi=mraa.Spi(0) #Bus comunication
spi.mode(mraa.SPI_MODE0) #Comunication MODE0
spi.frequency(2000000) #Frequency of 2MHz
spi.lsbmode(False) #Format data MSB


readCelsius(ss1)
readCelsius(ss2)
readCelsius(ss3)
readCelsius(ss4)


while (1):

	Rx=0
	Ry=0
	termopar1=0
	termopar2=0
	termopar3=0
	termopar4=0
	for interator in range(0,10):
		Rx  += 10000 * ((1024.0/(x.read()+1)) -1)
		Ry  += 10000 * ((1024.0/(y.read()+1)) -1)
		termopar1+=readCelsius(ss1)
		termopar2+=readCelsius(ss2)
		termopar3+=readCelsius(ss3)
		termopar4+=readCelsius(ss4)
		time_end= time.time()
		if (time_end- time_begin) < 1:
	     		time.sleep(1 - (time_end- time_begin)) 

                time_begin= time.time()
	Rx= Rx/10
	Ry= Ry/10
	termopar1= termopar1/10
	termopar2= termopar2/10
	termopar3= termopar3/10
	termopar4= termopar4/10
	
	mx=0
	mx= Rx_to_T(Rx)
	my= Ry_to_T(Ry)



	tempx= "%.2f" % mx
	tempy= "%.2f" % my
	#print (Rx)
	#print (Ry)
	print (tempx)
	print (tempy)
        print (termopar1)
        print (termopar2)
        print (termopar3)
        print (termopar4)
        ts= datetime.datetime.strftime(datetime.datetime.now(), '%d-%m %H:%M:%S')

	getifaces()
	# verifica se precisa de um novo ciclo
	clock_end= time.time()
        trun = clock_end- clock_begin
        #print(str(trun))
	if ((trun) >= 30*60 ):
		ciclo= ciclo +1
		cicloLog.seek(0)
		cicloLog.write(str(ciclo))
		cicloLog.flush()
		targetTemp = getTargetTemp(ciclo,l)
		clock_begin= clock_end

	media = (mx+ my)/2
	maior = my
	if ( mx > my):
		maior= mx
	
        if (maior < (targetTemp- 1) ):
		print('Ligar a resistencia')

                relay_pin.write(0)
		switch1= 1
	if (maior > (targetTemp - 0.5)):
		print('Desligar resistencia')
		switch1= 0
                relay_pin.write(1)
	count = count +1
	if (count > 6):
		count= 0
		f.write(ts)
		f.write(';'+ tempx)
		f.write(';'+tempy)
		f.write(';'+str(media))
		f.write(';'+str(switch1))
		f.write(';'+str(ciclo))
       		f.write(';'+str(targetTemp))
		f.write(';'+str(termopar1))
		f.write(';'+str(termopar2))
		f.write(';'+str(termopar3))
		f.write(';'+str(termopar4))

		f.write(';'+str(clock_end-clock_begin))
		f.write('\n')
		f.flush()


        	try:
	    		dweepy.dweet_for('NTC_UNIOESTE_02', {'tempx':tempx, 
'tempy': tempy,  'ifaces':ifaces, 'switch': switch1, 'targetTemp': 
targetTemp, 'ciclo': ciclo, 'termopar1':termopar1, 'termopar2': 
termopar2, 'termopar3': termopar3, 'termopar4': termopar4})
        	except:
            	    sys.stderr.write("Exception")
