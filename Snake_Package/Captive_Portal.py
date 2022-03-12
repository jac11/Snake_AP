#!/usr/bin/env python3

import subprocess
import sys
import os
import time 

Cap_port_Path = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Captive_Portal"
Root_Web      = "        DocumentRoot /var/www/html"
New_Root_Web  = "        #DocumentRoot /var/www/html"+'\n'+"        DocumentRoot "+ Cap_port_Path
Header = "#Snake_web_Portal"+'\n'+' <Directory "'+Cap_port_Path+'>'
Header2 = '#<Directory /var/www/html>'+'\n'+'<Directory "'+Cap_port_Path+'>'
line_replace = '<Directory /var/www/html>'
class Captive_Portal:
      
      def __init__(self):
         self.Captive_Pr_Set()
     
      def Captive_Pr_Set(self):
          print("[*] Captive Portal Mode in Precoess !!")
          with open ("/etc/apache2/sites-enabled/000-default.conf",'r') as config_server :
                    read_config = config_server.read()
                    if "#Snake_web_Portal"  not in read_config: 
                        with open ("/etc/apache2/sites-enabled/000-default.conf",'r') as FILE_RE :
                             FILE_RE_ACT  = FILE_RE.readlines()
                             for line in FILE_RE_ACT :                               
                                    line = line.replace(Root_Web,New_Root_Web)
                                    with open ("/etc/apache2/sites-enabled/000-default.txt",'a') as write_output:
                                         write_output_F = write_output.write(line) 
                        os.system("sudo a2enmod rewrite >/dev/null 2>&1")
                        with open ("/etc/apache2/sites-enabled/000-default.txt",'r') as read_output:
                                  read_out = read_output.read()                        
                        
                        with open('./rpache-rewrite.txt','r') as rpacherewrite :
                                  read_cont = rpacherewrite.read()
                        with open ("/etc/apache2/sites-enabled/000-default.conf",'w') as config_server :
                                   wireapacche = config_server.write( read_out+Header+read_cont)
                        with open("etc/apache2/apache2.conf",'r') Config_FIE :
                                 Read_Config_FILE = Config_FIE.readlines()
                                 for line in Read_Config_FILE :                               
                                     line = line.replace(line_replace,Header2)
                                     with open ("etc/apache2/apache2conf.txt",'a') as write_Config:
                                         write_output_F2 = write_Config.write(line) 
                        with open ("etc/apache2/apache2conf.txt",'r') as Reread_Config: 
                                  Read_Info = Reread_Config.read()
                        with open("etc/apache2/apache2.conf",'w') write_Config_FIE :
                                 Copy_Info = write_Config_FIE.write(Read_Info +'\n'+'ServerName  127.0.0.1')
                        os.system('sudo systemctl reload httpd.service >/dev/null 2>&1')
                        os.system("systemctl restart apache2 >/dev/null 2>&1")
                        os.remove("/etc/apache2/sites-enabled/000-default.txt")
                        os.remove("/etc/apache2/apache2conf.txt")
                        print("[+] Captive Portal Server is Up...") 
                    else:
                        os.system("systemctl restart apache2 >/dev/null 2>&1")
                        print("[+] Captive Portal Server is Up...") 
if __name__=='__main__':
   Captive_Portal()


