import pyupbit
import requests
import json
from flask import make_response

access = "aXKHw5tsr3uGwvZQ5bDq2qo5A0JPPTJUNkjj2CWD"
secret = "kt6gQfE1dJqenmte2DmXDtzE6DAoz9IPmYx9InMK"
upbit = pyupbit.Upbit(access, secret)

# 계좌 보유 금액
print(upbit.get_balance("KRW-BTC"))
print(upbit.get_balance("KRW"))

print("=======================================================")

# 종목 코드 정보
url = "https://api.upbit.com/v1/market/all"

querystring = {"isDetails": "false"}
headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring).json()
# response.raise_for_status()
# response.encoding = 'utf8'

# print(json.loads(response.text))

if len(response) > 0:
    f = open("files/items_code.txt", "a", encoding="utf8")
    for item in response:
        market = item["market"]
        korean_name = item["korean_name"]
        english_name = item["english_name"]

        f.write("%s\t%s\t%s\n" % (market, korean_name, english_name))
        # print("%s\t%s\t%s\n" % (market, korean_name, english_name))

    f.close()
