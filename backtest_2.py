import pyupbit
import numpy as np
import datetime
import pandas as pd

# 내 전략 백테스팅

# 1. 60분간의 평균 거래량 산출
# 2. 마지막 분봉의 거래량이 60분 평균 거래량의 10배 이상이고 양봉(시가 < 종가)이면 매수
# 3. 매수가격 저장
# 4. 매도 이전까지 1~3조건이 실행되지 않도록 차단
# 5. 익절매도조건
#     > 음봉이며, 종가가 고가대비 70% 이하로 떨어졌을 때
# 6. 손절매도조건
#     > 매수가대비 -3% 이상 하락하였을 때

def calc_avg_vol(df):
    sum = 0
    for i in range(1, 60):
        sum += df['volume'].shift(i)
    return sum / 60

st = datetime.datetime.now().timestamp()

# ohlcv(open, high, low, close, volume) 시가, 고가, 저가, 종가, 거래량 데이터 받아오기
df = pyupbit.get_ohlcv("KRW-ELF", "minute1", 200)
ed = datetime.datetime.now().timestamp()
print(df)
print("소요시간 : ", ed - st)

# sum = 0
# for i in range(1, 60):
#     sum += df['volume'][len(df) - i]

df['avg_vol'] = np.where(df.index >= df.index[60], calc_avg_vol(df), 0)

# pd.set_option('display.max_row', 500)
# pd.set_option('display.max_columns', None)
# print(df)

# df['size'] = np.where(df.index > df.index[len(df)-3], 1, 2)

# # 평균 거래량 계산
# df['avgVol'] = (df['high'] - df['low']) * 0.5
#
# # target(매수가), range 컬럼을 한 칸씩 밑으로 내림(.shift(n))
# df['target'] = df['open'] + df['range'].shift(1)
#
# fee = 0.0005  # 거래 수수료
#
# # np.where(조건, true 반환값, false 반환값) -> 3항연산자와 같은 기능
# df['ror'] = np.where(df['high'] > df['target'],
#                      df['close'] / df['target'] - fee,
#                      1)
# # 누적 곱 계산(cumprod) => 누적수익률
# df['hpr'] = df['ror'].cumprod()
#
# # Drow Down 계산 (누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100)
# df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#
# # MDD계산
# print("MDD(%): ", df['dd'].max())
#
# # 엑셀로 저장
df.to_excel("test_result.xlsx")




