#!/bin/usr/env python3
from subprocess import PIPE
import subprocess
import os 
import time
class Show_AP_all :
      def __init__(self):
         self.Get_wifi()
      def Get_wifi(self):
          print("\n[*] all access point - Bssid - ssid - channal -  signal "+'\n')
          command  = "nmcli d wifi | tee outputee.txt"
          subprocess.call( command,shell=True,stderr=subprocess.PIPE,stdout=PIPE)
          print(" "+"-"*81) 
          print("| "+f"{'   BSSID    ':<23}","| "+f"{'    SSID    ':<21}"+" | "+f"{'  Channal  ':<12}"," | "+f"{'  SIGNAL  ':<12}""  |")
          print(" "+"-"*81)
          count = 0
          with open("outputee.txt",'r') as data_file:
               for line in data_file:
                   count +=1
                   time.sleep(0.20)
                   data = line.split()
                   bssid,ssid,channal,saginel = data[0].replace('IN-USE',''),data[1].replace('BSSID',''),data[3].replace('MODE',''),data[6].replace('SIGNAL','')
                   print("| "+' '+f"{ bssid:<22}","| "+' ' +f"{ ssid[0:20]:<20}"+" | "+'   '+f"{ channal:<9}"," | "+'   '+f"{ saginel:<9}""  |")
          os.remove('outputee.txt') 
          print('\n\n'+'='*30+'\n\n'+'[*] total access point -----|> ', str(count))  
if __name__=='__main__':
   Show_AP_all()
