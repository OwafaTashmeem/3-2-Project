#2nd function named main2.py
#from PIL import ImageGrab
from time import sleep
a="OFF"
def buzz(a):
  import serial
  arduinoData=serial.Serial('com8 ' , 115200)
  while(True):
   sleep(1.6)
   #Amd=input ( 'Please Enter Your Command:') 
   cmd=a +'\r'
   arduinoData.write(cmd. encode( ))
   break
  sleep(2)
  cmd="OFF"+'\r'
  arduinoData.write(cmd. encode( ))

def mayday(a):
  import serial
  arduinoData=serial.Serial('com8 ' , 115200)
  while(True):
   sleep(1.6)
   #Amd=input ( 'Please Enter Your Command:') 
   cmd=a +'\r'
   arduinoData.write(cmd. encode( ))
   break
def phew(a):
  import serial
  arduinoData=serial.Serial('com8 ' , 115200)
  while(True):
   sleep(1.6)
   #Amd=input ( 'Please Enter Your Command:') 
   cmd=a +'\r'
   arduinoData.write(cmd. encode( ))
   break  
  
  
  #cmd="OFF"+'\r'
  #arduinoData.write(cmd. encode( ))


#buzz("ON")