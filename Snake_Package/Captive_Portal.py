#!/usr/bin/env python3


import sys
import os
import subprocess
from subprocess import PIPE

Status_access = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package/ServerLog/log_access.log"
Status_error = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package/ServerLog/log_error.log"
LOG_PATH = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package"

class Captive_Portal:
    def __init__(self):

        self.CheckStutas()

    def FileWrite(self):

        with open (f'{LOG_PATH}/resources/portal.conf' ,'r') as readpath,\
        open('/etc/apache2/sites-enabled/portal.conf' ,'w') as writepath:
            getpath = readpath.read().replace('ErrorLog', f'ErrorLog {Status_error}').replace('CustomLog', f'CustomLog {Status_access}')
            writepath.write(getpath)

    def Once_done(self):

        command1 = 'sudo a2enmod dump_io >/dev/null 2>&1'
        subprocess.call(command1,shell=True,stderr=subprocess.PIPE)
        os.system('sudo systemctl reload httpd.service >/dev/null 2>&1')
        os.system("systemctl restart apache2 >/dev/null 2>&1")
        command = "sudo a2enmod dumpio >/dev/null 2>&1"
        subprocess.call(command,shell=True,stderr=subprocess.PIPE)
        command3 = 'sudo a2ensite 000-Porat.conf >/dev/null 2>&1'
        subprocess.call(command3,shell=True,stderr=subprocess.PIPE)
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

    def CheckStutas(self):

        if os.path.exists('/etc/apache2/sites-enabled/portal.conf'):
            with open('/etc/apache2/sites-enabled/portal.conf','r') as CheckPass:
                CheckPass = CheckPass.read()
                if  Status_access in CheckPass:
                    print('[+] Captive_Portal Config Found')
                else:
                    print('[+] Captive_Portal Config Update')
                    self.FileWrite()
                    self.Once_done()                  
        else:   
            print('[+] Captive_Portal Config Create') 
            self.FileWrite()
            self.Once_done()
if __name__=='__main__':
   Captive_Portal()


