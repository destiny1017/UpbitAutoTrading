import pyupbit
import requests
import json
import time
from flask import make_response

upbit_keys = open("C:/upbit/access_key", "r", encoding="utf8")

access = upbit_keys.readline().rstrip('\n')
secret = upbit_keys.readline()
upbit = pyupbit.Upbit(access, secret)

# 계좌 보유 금액
print(upbit.get_balance("KRW-BTC"))
print(upbit.get_balance("KRW"))

print("=======================================================")

# 종목 코드 정보
# url = "https://api.upbit.com/v1/market/all"
#
# querystring = {"isDetails": "false"}
# headers = {"Accept": "application/json"}
#
# response = requests.request("GET", url, headers=headers, params=querystring).json()
# response.raise_for_status()
# response.encoding = 'utf8'

# print(json.loads(response.text))

# 종목 정보 파일 저장
# if len(response) > 0:
#     f = open("files/items_code.txt", "a", encoding="utf8")
#     for item in response:
#         market = item["market"]
#         korean_name = item["korean_name"]
#         english_name = item["english_name"]
#
#         f.write("%s\t%s\t%s\n" % (market, korean_name, english_name))
#         # print("%s\t%s\t%s\n" % (market, korean_name, english_name))
#
#     f.close()

# minute1 = pyupbit.get_ohlcv("KRW-SSX", "minute1")
# print(minute1)
# print(type(minute1), minute1.shape)
# print(minute1.index[-1:])

# for min in minute1.values.tolist():
#     print(min)
# while True:
#     minute1 = pyupbit.get_ohlcv("KRW-SSX", "minute1").values.tolist()
#     print(minute1[-1:])
#     time.sleep(1)

last_min = None
while True:
    minute1 = pyupbit.get_ohlcv("KRW-SSX", "minute1", 1)
    print(minute1)
    current_min = minute1.index
    if last_min != current_min:
        print("changed min...")

    print(current_min)
    last_min = current_min
    time.sleep(1)

# >> 1분마다 반복 알고리즘
# 1. 최근 30분간의 1분 평균 거래량 산출
# 2. 마지막의 1분봉 거래량이 1에서 산출한 거래량의 4배 이상이고 양봉인 종목 검색
