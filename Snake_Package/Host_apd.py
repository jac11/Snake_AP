#!/usr/bin/env python3

import os
import time
from subprocess import PIPE
import subprocess
Banner = """
        __
       {0O}
       \__/
       /^/  SNAKE ACCESS POINT START
      / /____  TO exit  CTRL+C   
     (_______) BY : JACSTROY
   _(_________)_ 
  (_____________)0o    
          _     
         (_)  
"""
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
