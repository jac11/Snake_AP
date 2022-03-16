#!/usr/bin/env python3

import os
import time
from subprocess import PIPE
import subprocess
from banner import *

print (Banner)

try:
    Start_FAP = "sudo hostapd hostapd.conf "
    os.system(Start_FAP)
except KeyboardInterrupt:
   Command  = [
                "sudo airmon-ng stop wlan0mon",
                " sudo service NetworkManager restart",
               ]
   for _ in Command : 
      subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
   
   print("[*] FAKE ACCESS POINT EXIT ...!!")
   time.sleep(3)
   exit() 
