#!/usr/bin/env python3

import os
import sys
import time
import subprocess
from subprocess import PIPE

Path_St = "/".join(os.path.abspath(__file__).split('/'))[:-16]

class Read_Stream_Update :

       def __init__(self):
           self.while_read()
       def while_read(self):
          try:
              while True :
                 remotefile = Path_St +'read_errorLOG.py > '+ Path_St+'LOGIN_DB.txt'
                 call_termminal = subprocess.call(remotefile,shell=True,stderr=subprocess.PIPE)
                 with open(Path_St+'LOGIN_DB.txt','r') as filedb :
                    db_file = filedb.read()
                    os.system('clear')
                    print('\n'+('='*20)+'\n[+] Important Note '+'\n'+('='*20)+'\n'+'[+] This File read in real Time will be Update evey 30 Seconds'\
                    +'\n'+('='*40)+'\n'+db_file)
                    time.sleep(30)
          except KeyboardInterrupt :
              exit() 
if __name__=='__main__':
   Read_Stream_Update()
      

 
