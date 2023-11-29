import senko
import wifimgr
from machine import UART, Pin, ADC, I2C
from machine import WDT, reset
import utime
from time import sleep
from ntptime import settime

OTA = senko.Senko(
  user="lysistech", # Required
  repo="environment", # Required
  branch="main", # Optional: Defaults to "master"
  files = ["main.py"]
)

try:
  import usocket as socket
except:
  import socket

def deepsleep (duration):
    try:
        import machine
        #print('Going to Deep Sleep now...')
        machine.deepsleep(duration) #milliseconds
    except:
        utime.sleep_ms(500) 

wdt = WDT(timeout=1000000)  # enable it with a timeout of 16,66 min. 


wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")

values = range(200)
sl=10000

try:
 settime()
 print("Internet ok, Time Set!!!!!")
except:
  print("No Internet, Time not Set. Retrying in 20 sec.......")
  for i in values:  
      utime.sleep_ms(sl)  #deepsleep(20000)
      wlan = wifimgr.get_connection()
      if wlan is None:
         print("Could not initialize the network connection. Retrying in 10 sec......")
      else:
        break
      if i>50:
        sl=60000
      if i>100:
        sl=360000  

while (1):

  if OTA.update():
      print("Updated to the latest version! Rebooting...")
      machine.reset()
  else:
     print("No UPDATES Detected@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

  print("Going to sleep............................")
  utime.sleep_ms(30000)     #30 sec.

wdt.feed()



