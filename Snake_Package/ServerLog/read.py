print(" "+"-"*55) 
print("| "+f"{'       EMAIL    ':<25}","| "+f"{'         PASSOWRD   ':<25} |")
print(" "+"-"*55)

with open('log_error.log') as f :
     a = f.readlines()
for line in a :
    if "auth_" in  line :
        line = line.split('auth_user=')
        line = str(line[-1]).split('auth_pass=')
        line = str(line).replace('&accept=Login','').replace('%40','@').replace('&',' ')\
        .replace('\\n','').replace("['",'').replace("']",'').replace("'",'').split(',')
        print("| "+"  "+f"{   line[0]    :<23}","| "+"  "+f"{      line[1]    :<23} |")
